<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
     version="1.0">
<xsl:output method="xml"
	doctype-system="http://www.oasis-open.org/docbook/xml/4.4/docbookx.dtd" 
	doctype-public="-//OASIS//DTD DocBook XML//EN"/>  
<xsl:template match="doxygen">
<part>
	<title>Ductape API</title>
	<xsl:for-each select="compounddef">		
			<reference>
				<title><xsl:value-of select="compoundname"/></title>
				<refentry>
					<refnamediv>
						<refname><xsl:value-of select="compoundname"/></refname>
						<refpurpose />
					</refnamediv>
				<xsl:text>
	</xsl:text>
				<!--start reference entry -->
				<refsect1><title></title><para /></refsect1>	
				<xsl:for-each select="sectiondef/memberdef">		
					<xsl:element name="refsect1">
						<xsl:attribute name="id"> 
							<xsl:for-each select="@id">
								<xsl:value-of select="." />
							</xsl:for-each>
						</xsl:attribute>
					<!--reference metadata -->
						<title><xsl:value-of select="name"/></title>
					<xsl:text>
		</xsl:text>
						<funcsynopsis>
						<xsl:text>
				</xsl:text>
							<funcprototype>
							<xsl:text>
					</xsl:text>
								<funcdef>
								<xsl:text>
						</xsl:text>
									<function>
										<xsl:value-of select="definition" />
									</function>
									<xsl:text>
					</xsl:text>
								</funcdef>
								<xsl:text>
					</xsl:text>
									<xsl:choose>
										<xsl:when test="param">
											<paramdef>
								<xsl:text>
						</xsl:text>
											<xsl:for-each select="param">
												<xsl:value-of select="type" />
												<parameter><xsl:value-of select="declname" /></parameter>
											</xsl:for-each>
											</paramdef>
										</xsl:when>
										<xsl:otherwise>
											<void />
										</xsl:otherwise>
									</xsl:choose>
									<xsl:text>
					</xsl:text>
								<xsl:text>
				</xsl:text>
							</funcprototype>
							<xsl:text>
			</xsl:text>
						</funcsynopsis>
						<xsl:text>
			</xsl:text>
						<refsect2>
						<xsl:text>
				</xsl:text>
							<title><xsl:for-each select="name" /></title>
                     <xsl:for-each select="briefdescription">
							<xsl:text>
				</xsl:text>
					 			<synopsis><xsl:apply-templates/></synopsis>
								<xsl:text>
				</xsl:text>
							</xsl:for-each>
							<xsl:for-each
							select="detaileddescription/para">
								<xsl:for-each select="/parameterlist/parameteritem">
								<xsl:text>
				</xsl:text>
									<para>Parameters:</para>
									<xsl:text>
				</xsl:text>
									<xsl:text>
					</xsl:text>
										<refsect2>
										<xsl:text>
						</xsl:text>
											<title></title>
											<para><xsl:value-of
											select="parameternamelist/parametername"/>
											<xsl:value-of
											select="parameterdescription"/></para>
											<xsl:text>
					</xsl:text>
										</refsect2>
										<xsl:text>
				</xsl:text>
								</xsl:for-each>
								<xsl:text>
				</xsl:text>
								<xsl:for-each select="simplesect">
									<xsl:choose>	
										<xsl:when test="@kind='return'">
											<para>Returns:</para>
											<xsl:text>
				</xsl:text>
											<para><xsl:value-of select="para" /></para>
										</xsl:when>
										<xsl:when test="@kind='see'">
											<para>See Also:</para>
											<xsl:text>
				</xsl:text>
											<para>
											<xsl:if test="para/ref">
											<xsl:text>
					</xsl:text>
											<refsect2>
													<xsl:for-each select="para">
														<xsl:for-each select="ref">
														<xsl:text>
						</xsl:text>
															<xsl:text>
							</xsl:text>
																<para>
																<xsl:text>
								</xsl:text>
																	<xsl:element name="xref">
																		<xsl:attribute name="linkend">
																			<xsl:for-each select="@refid">
																				<xsl:value-of select="." />
																			</xsl:for-each>
																		</xsl:attribute>
																	</xsl:element>
																	<xsl:text>
							</xsl:text>
																</para>
																<xsl:text>
						</xsl:text>
													</xsl:for-each>
												</xsl:for-each>
												</refsect2>
													<xsl:text>
					</xsl:text>
											</xsl:if>
											<xsl:text>
				</xsl:text>
											</para>
											<xsl:text>
				</xsl:text>
										</xsl:when>
										
									</xsl:choose>
								</xsl:for-each>
							</xsl:for-each>
                     <xsl:for-each select="inbodydescription">
								<para><xsl:apply-templates/></para>
							</xsl:for-each>
							<xsl:text>
			</xsl:text>
						</refsect2>
						<xsl:text>
		</xsl:text>
					<xsl:for-each select="enumvalue">
					<xsl:text>
		</xsl:text>
						<refsect2>
							<xsl:text>
			</xsl:text>
							<title><xsl:value-of select="name"/></title>
							<xsl:for-each select="briefdescription">
							<xsl:text>
			</xsl:text>
								<synopsis><xsl:apply-templates/></synopsis>
							</xsl:for-each>
							<xsl:text>
			</xsl:text>
							<xsl:for-each select="briefdescription">
							   <para><xsl:apply-templates/></para>
								<xsl:text>
		</xsl:text>
							</xsl:for-each>
						</refsect2>
					</xsl:for-each>
					<refsect2><title/><para/></refsect2>
					<xsl:text>
	</xsl:text>
					</xsl:element>
					<xsl:text>
	</xsl:text>
			</xsl:for-each>
	</refentry>
</reference>
		</xsl:for-each>
</part>
	</xsl:template>
</xsl:stylesheet>
