#!/bin/sh

#*******************************************#
#            upload-to-website              #
#       written by: Scott Biersdorff        #
#              July 15 2005                 #
#                                           #
#         Automaticlly upload docbook       #
#             files to a website            #
#*******************************************#

#*******************************************#


#*******************************************#
#                                           #
#  Path varibles are define like:           #
#  des_full = des + dir_name                #
#  source_full = source + dir_name          #
#                                           #
#  ALL UPPERCASE varibles are the script's  #
#  arguments.                               #
#                                           #
#*******************************************#

#current directory
current_dir=`pwd`

#*******************************************#
# Function: help                            #
# Arguments: none                           #
# returns: none                             #
#                                           #
#DESCRIPTION: print out help page then exits#
#                                           #
#*******************************************#
help()
{
  cat <<HELP
upload-to-website -- Automaticlly upload docbook files to a website.

USAGE: upload-to-website [-f [directory name]] [-vh] [source directory] [destination directory]

NOTE:  when uploading to a remote directory the destination directory must
       be of the form: [user@][host]:[path] (same as scp). 

DESCRIPTION: upload-to-website script is designed to easily publish
          docbook's xml documents to a web server. this script does the
          following: 
            1.issue 'make html-chunked' on these xml files 
            2.create aappropriate directory structure 
            3.place each of the different html pages with the required
              images into a separate directories 
            4. copy all the web-pages to the web server.

          if the xml files are structure like this:

            /docbook/user-guide/user-guide.xml
            /docbook/new/tau/tutorial.xml

          and 'upload-to-website -r /docbook web-server.com:/www/docs' is issued

          then the resulting directory structure on web-server.com would be:

            /www/docs/user-guide/
            /www/docs/tutorial/


OPTIONS:  -f [directory name] Specifes the name of the destiation directory.
             Cannot be used with -r option.

          -r Recursivly uploads docbook file to the website. ie. every 
             subdirectoy of [source directory] called _ -chunked is added
             to the website. Cannot be used with -f option.

          -h help.

EXAMPLES: publish xml documentation in 'ktau' directory to 
          'user@nic.uoregon.edu:/www/website/documentation'

          'upload-to-website ktau user@nic.uoregon.edu:/www/website/documentation'

          publish all xml documents in '/User/docbook' to 'Sites/docs'

          'upload-to-website -r /User/docbook Sites/docs' 

BUGS:     The docbook html files must be chunked into the directory called,
          [source directory]-chunked. This is only true if the $TARGET
          varible set in the docbook makefile is set to the same name as the 
          directory in which it resides. This problem should be solved when
          the recursive feature is intergrated.

          The script does not produce any useful error messages.

DIAGNOSIS:upload-to-website exit with error number 1 if any errors occurs.

HELP
  exit 0
}

#****************************************************#
#                                                    #
#  Function: recurse                                 #
#  Arguments: none                                   #
#  Returns: none                                     #
#                                                    #
#     Calls copy-files and move_file sript on every  #
#     subdirectoy, with chunked html files, of       #
#            the specifed source file.               #
#                                                    #
#****************************************************#
recurse()
{
  echo "recursing..."
  for DIR in `find $current_dir -type d | grep chunked`; 
  do
    DIR_NAME=`echo $DIR | sed 's/[A-Za-z\/]*\/\([A-Za-z]*\)-chunked/\1/'`
    echo "DIR_NAME: $DIR_NAME"
    copy_files $DIR $DESTINATION/$DIR_NAME $DIR_NAME
  done

  move_files $DESTINATION

}


#****************************************************#
#                                                    #
#   Copy the generated html files to the web host.   #
#                                                    #
#   arguments: source destiation and directory name. #
#                                                    #
#****************************************************#
copy_files()
{  

  #copy file securily to website host.

  source=$1
  des_full=$2
  dir_name=$3

#****************************************************#
#                                                    #
#   Frist create directory structure on remote host. #
#                                                    #
#   There are three possiblite formats for the:      #
#   destination locatation:                          #
#   1. host:dir                                      #
#   2. dir (local transfer)                          #
#                                                    #
#****************************************************#

  #parse destiation by spliting on ':'
  str=$(echo $des_full | awk -F, 'BEGIN { FS=":" } { print $1 "\n" $2 }' )
  array=($str);
  host=${array[0]}
  dir=${array[1]}

  #*************************************************************
  #make temp directory .temp
  #*************************************************************
  mkdir -p $current_dir/.temp/$dir_name

  if [ -n "$host" ] && [ -n "$dir" ] ; then
    mkdir -p .temp/$dir
  else
    mkdir .temp/$DIR_NAME
  fi

  #*************************************************************
  #copy html files  
  #*************************************************************
  for file in `ls $source`
  do
    #if file needs to be updated.
    if [ $source/$file -nt $des/$file ] 
    then
      echo "copy file: $file to: .temp/$dir_name"
      arg=`echo $current_dir/.temp/$dir_name/. | sed -e 's_\/\/_\/_g' -e 's_\/-_-_g'`
      echo "cp $source/$file $arg"
      cp $source/$file $arg
    fi
  done
  #*************************************************************
  #copy docbook image files
  #*************************************************************
  for file in `ls $current_dir/tools/docbook-xsl-1.68.1/images/ | grep *.tiff`
  do
    #if images need to be updated.
    if [ $current_dir/tools/docbook-xsl-1.68.1/images/$file -nt $des/$file ]
    then   
      echo "copy file: $file to: .temp/$dir_name"
      arg=`echo $current_dir/.temp/$dir_name/. | sed -e 's_\/\/_\/_g' -e 's_\/-_-_g'`

      echo "cp $current_dir/tools/docbook-xsl-1.68.1/images/$file $arg"
      cp $current_dir/tools/docbook-xsl-1.68.1/images/$file $arg
    fi
  done
}

#*************************************************************
#
#  Function: move_files
#  Arguments: destination directory (can be remote)
#  Returns: none
#  uses scp to copy files from source to destiation 
#
#*************************************************************
move_files()
{
  des=$1
 
  #securely copy file from .temp directory to destination directory.
  scp -r $current_dir/.temp/* $des/.

  #remove temp files
  rm -rf $current_dir/.temp
}


#**************************************************************
#begain scripting
#**************************************************************
#if we have less than two arguments print help text.
if [ $# -lt 2 ] ; then
  help 
fi


#**************************************************************
#parse options
#**************************************************************
while [ -n "$1" ]; do
  case $1 in
    -r) r=1; shift 1;;
    -f) DIR_NAME=$2; shift 2;; # -f takes an argument	
    -h) help; shift 1;; 
    --) shift;break;; # end of options
    -*) echo "error: no such option $1. -h for help";exit 1;;
    *)  break;;
  esac
done


#**************************************************************
#handle arguments
#**************************************************************
#if -f is not set.

# -f option is set.
if [ -n "$DIR_NAME" ] ; then

  #confrim that there are three arguments
  if [ $# -lt 2 ] ; then 
    echo "ERR: option -f requires a thrid argument."
    exit 1 #exit with error
  fi

  #set source and destination varibles.
  SOURCE=$1
  DESTINATION=$2

else # -f option is not set.

  SOURCE=$1
  DESTINATION=$2

  #defult destination directory name.
  DIR_NAME=$SOURCE
fi
#**************************************************************
#check for input errors
#**************************************************************

if [ ! -d "$SOURCE" ] 
then
  echo "SOUCRE directory not found."
  exit 1
fi

#**************************************************************
#debuging output
#**************************************************************
echo "DIR_NAME is = $DIR_NAME"
echo "SOURCE is = $SOURCE"
echo "DESTINATION is = $DESTINATION"

#Makes docbook docuemnets into html.
cd $SOURCE ; make html-chunked ; cd $current_dir 

if [ "$r" = "1" ] ; then 
  recurse

else 
  #find *-chunked directory
  full_source=`find $current_dir/$SOURCE -type d | grep chunked`

  #remove ending '/' from source varible. -SB: is there a consistant way to do this?
  len=`expr "$SOURCE" : '.*'`
  short=`echo $SOURCE | cut -c 1-$len`
  full_soucre=`echo $full_source | sed 's_ [^ ]*__g'`
	
	echo $full_source
  
	if [ ! -d "$full_source" ]
  then
    echo "ERR: cannot find xml files in SOURCE directory."
    exit 1
  fi

  #remove any double '/'. or '/-'
  arg=`echo $full_source | sed -e 's_\/\/_\/_g' -e 's_\/-_-_g'`


  copy_files $arg $DESTINATION/$DIR_NAME $DIR_NAME

  move_files $DESTINATION

fi
exit 0


