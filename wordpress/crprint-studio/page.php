<?php
if(!defined('ABSPATH'))exit;get_header();
while(have_posts()){the_post();$layout=get_post_meta(get_the_ID(),'_crprint_layout',true);
    if($layout){echo crprint_markup(apply_filters('the_content',get_the_content()));}
    else{echo '<section class="section"><div class="container prose"><h1>'.esc_html(get_the_title()).'</h1>';the_content();echo '</div></section>';}
}
get_footer();
