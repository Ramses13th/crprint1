<?php if(!defined('ABSPATH'))exit; ?><!doctype html><html <?php language_attributes(); ?>><head><meta charset="<?php bloginfo('charset'); ?>"><meta name="viewport" content="width=device-width, initial-scale=1"><?php wp_head(); ?></head><body <?php body_class('wordpress-site'); ?>><?php wp_body_open();
$markup=crprint_template_html('header');
if(has_nav_menu('primary')){
    $menu=wp_nav_menu(array('theme_location'=>'primary','container'=>false,'items_wrap'=>'%3$s','echo'=>false));
    $markup=preg_replace_callback('/(<nav id="primary-navigation"[^>]*>).*?(<\/nav>)/s',function($m)use($menu){return $m[1].$menu.$m[2];},$markup);
}
$markup=preg_replace('/<a class="icon-button cart-link".*?<\/a>/s',crprint_cart_link(),$markup);
echo $markup;
?><main id="main">
