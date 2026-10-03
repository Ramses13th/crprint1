<?php if(!defined('ABSPATH'))exit; ?></main><?php
$markup=crprint_template_html('footer');
$markup=preg_replace('/<p class="local-tools".*?<\/p>/s','',$markup);
$markup=str_replace('Termeni demo','Termeni și condiții',$markup);
echo $markup;wp_footer();?></body></html>
