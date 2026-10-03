<?php
if(!defined('ABSPATH'))exit;get_header();echo '<section class="section"><div class="container prose">';
if(have_posts()){while(have_posts()){the_post();echo '<article><h1><a href="'.esc_url(get_permalink()).'">'.esc_html(get_the_title()).'</a></h1>';the_content();echo '</article>';}the_posts_pagination();}
else{echo '<h1>Pagina nu a fost găsită.</h1><p><a href="'.esc_url(home_url('/')).'">Înapoi la atelier ↗</a></p>';}
echo '</div></section>';get_footer();
