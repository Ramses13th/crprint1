<?php
if(!defined('ABSPATH'))exit;get_header();
if(have_posts()){while(have_posts()){the_post();$content=get_the_content();echo $content?crprint_markup(apply_filters('the_content',$content)):do_shortcode(crprint_template_html('index'));}}
else{echo do_shortcode(crprint_template_html('index'));}
get_footer();
