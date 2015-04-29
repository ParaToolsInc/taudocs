<?xml version='1.0'?>
  <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"> 

  <xsl:import href="../tools/docbook-xsl-1.69.1/html/docbook.xsl"/>

  <xsl:template name="user.header.content">
    <xsl:text disable-output-escaping="yes">
       &lt;?php include("../../header.php") ?>
       &lt;div id="content">
    </xsl:text>
  </xsl:template>


  <xsl:template name="user.footer.content">
    <xsl:text disable-output-escaping="yes">
       &lt;/div>
       &lt;?php include("../../footer.php") ?>
    </xsl:text>
  </xsl:template>

</xsl:stylesheet> 
