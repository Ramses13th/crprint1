<?php
if (!defined('ABSPATH')) { exit; }
add_action('after_setup_theme', function () {
    add_theme_support('title-tag'); add_theme_support('post-thumbnails');
    add_theme_support('woocommerce'); add_theme_support('wc-product-gallery-slider');
    add_theme_support('html5', array('search-form','comment-form','gallery','caption','style','script'));
    register_nav_menus(array('primary'=>'Navigare principală'));
});
function crprint_asset($path) { return trailingslashit(get_template_directory_uri()).'assets/'.ltrim($path,'/'); }
function crprint_link($key) {
    if ($key==='index') { return home_url('/'); }
    if (function_exists('wc_get_page_permalink')) {
        if ($key==='magazin') { return wc_get_page_permalink('shop'); }
        if ($key==='cos') { return wc_get_cart_url(); }
        if ($key==='checkout') { return wc_get_checkout_url(); }
        if ($key==='produs-nava') { $id=wc_get_product_id_by_sku('nava-24-septembrie'); return $id && get_post_status($id)==='publish' ? get_permalink($id) : wc_get_page_permalink('shop'); }
    }
    $ids=get_option('crprint_page_ids',array());
    return isset($ids[$key]) ? get_permalink($ids[$key]) : home_url('/'.$key.'/');
}
function crprint_markup($markup) {
    $asset=crprint_asset('');
    $markup=str_replace(array('"images/',' images/','"models/'),array('"'.$asset.'images/',' '.$asset.'images/','"'.$asset.'models/'),$markup);
    $markup=str_replace('NAVA%2024%20SEPTEMBRIE.fbx','nava-preview.glb',$markup);
    $markup=preg_replace_callback('/href="([a-z0-9-]+)\.html(?:\?id=([^"#]+))?(#[^"]*)?"/',function($m){
        $url=crprint_link($m[1]);
        if($m[1]==='produs-nava' && !empty($m[2]) && function_exists('wc_get_product_id_by_sku')) { $id=wc_get_product_id_by_sku(rawurldecode($m[2])); if($id && get_post_status($id)==='publish') $url=get_permalink($id); }
        return 'href="'.esc_url($url.($m[3]??'')).'"';
    },$markup);
    return $markup;
}
function crprint_template_html($key) {
    $file=get_template_directory().'/layouts/'.sanitize_file_name($key).'.html';
    return is_file($file) ? crprint_markup(file_get_contents($file)) : '';
}
add_action('wp_enqueue_scripts',function(){
    $base=get_template_directory();
    wp_enqueue_style('crprint-design',crprint_asset('design.css'),array(),filemtime($base.'/assets/design.css'));
    wp_enqueue_style('crprint-woo',crprint_asset('wordpress.css'),array('crprint-design'),filemtime($base.'/assets/wordpress.css'));
    wp_enqueue_script('crprint-ui',crprint_asset('script.js'),array(),filemtime($base.'/assets/script.js'),array('strategy'=>'defer','in_footer'=>true));
    wp_add_inline_script('crprint-ui','window.crprintConfig='.wp_json_encode(array('assets'=>crprint_asset(''))).';','before');
    if(class_exists('WooCommerce')) wp_enqueue_script('wc-cart-fragments');
});
function crprint_cart_link(){
    $count=function_exists('WC') && WC()->cart?intval(WC()->cart->get_cart_contents_count()):0;
    $label='Coș de cumpărături, '.$count.($count===1?' produs':' produse');
    return '<a class="icon-button cart-link" href="'.esc_url(crprint_link('cos')).'" aria-label="'.esc_attr($label).'"><svg class="icon" aria-hidden="true"><use href="#icon-bag"></use></svg><span data-cart-count aria-hidden="true">'.$count.'</span></a>';
}
add_filter('woocommerce_add_to_cart_fragments',function($fragments){
    $fragments['a.cart-link']=crprint_cart_link();
    return $fragments;
});
add_action('wp_head',function(){
    echo '<meta name="theme-color" content="#121315"><link rel="icon" type="image/png" href="'.esc_url(crprint_asset('images/logo-og-512.png')).'">';
    echo '<script>try{document.documentElement.dataset.theme=localStorage.getItem("crprint-theme")||"dark"}catch(e){}</script>';
    echo '<script type="importmap">'.wp_json_encode(array('imports'=>array('three'=>crprint_asset('vendor/three/build/three.module.js'),'three/addons/'=>crprint_asset('vendor/three/examples/jsm/'))),JSON_UNESCAPED_SLASHES).'</script>';
    if(!defined('WPSEO_VERSION') && !defined('RANK_MATH_VERSION')) {
        $description=is_singular()?get_post_meta(get_queried_object_id(),'_crprint_description',true):'';
        if(!$description)$description='Printare FDM și SLA, modelare și scanare 3D în Constanța. CR Print 3D · hi@crprint.ro · 0735 961 151.';
        echo '<meta name="description" content="'.esc_attr($description).'"><meta property="og:title" content="'.esc_attr(wp_get_document_title()).'"><meta property="og:description" content="'.esc_attr($description).'"><meta property="og:type" content="website"><meta property="og:locale" content="ro_RO"><meta property="og:image" content="'.esc_url(crprint_asset('images/crprint-atelier-generated.webp')).'"><meta name="twitter:card" content="summary_large_image">';
    }
    if(is_front_page() && !defined('WPSEO_VERSION') && !defined('RANK_MATH_VERSION')) {
        $schema=array('@context'=>'https://schema.org','@type'=>'LocalBusiness','name'=>'CR Print 3D','url'=>home_url('/'),'telephone'=>'+40735961151','email'=>'hi@crprint.ro','address'=>array('@type'=>'PostalAddress','streetAddress'=>'Bravilor 4','addressLocality'=>'Constanța','addressCountry'=>'RO'),'openingHoursSpecification'=>array(array('@type'=>'OpeningHoursSpecification','dayOfWeek'=>array('Monday','Tuesday','Wednesday','Thursday','Friday'),'opens'=>'10:00','closes'=>'18:00')));
        echo '<script type="application/ld+json">'.wp_json_encode($schema).'</script>';
    }
},2);
add_filter('wp_robots',function($robots){if(function_exists('is_cart') && (is_cart()||is_checkout()||is_account_page())) { $robots['noindex']=true; $robots['nofollow']=true; }return $robots;});
add_action('woocommerce_after_single_product_summary',function(){
    global $product;
    if($product && str_starts_with($product->get_sku(),'nava-24-septembrie')) echo '<section class="product-3d"><p class="eyebrow">PREVIZUALIZARE SIMPLIFICATĂ</p><h2>Fiecare unghi contează.</h2>'.crprint_template_html('viewer').'</section>';
},8);
add_shortcode('crprint_store_showcase',function(){
    if(!function_exists('wc_get_products'))return '<p>Magazinul este în pregătire. Contactează-ne pentru detalii.</p>';
    $products=wc_get_products(array('status'=>'publish','limit'=>2,'orderby'=>'date','order'=>'ASC'));
    if(!$products)return '<div class="demo-banner"><p>Colecția este în pregătire. Produsele vor apărea după publicare în WooCommerce.</p></div>';
    $out='<div class="catalog-grid">';
    foreach($products as $product){$out.='<article class="product-card"><a class="product-card-image" href="'.esc_url($product->get_permalink()).'">'.$product->get_image('woocommerce_single').'</a><div class="product-card-body"><h3><a href="'.esc_url($product->get_permalink()).'">'.esc_html($product->get_name()).'</a></h3><div class="product-card-bottom"><strong>'.$product->get_price_html().'</strong><a class="button button-small button-ghost" href="'.esc_url($product->get_permalink()).'">Descoperă ↗</a></div></div></article>';}
    return $out.'</div>';
});

add_filter('woocommerce_show_page_title',function($show){return is_shop()?false:$show;});
add_filter('document_title_parts',function($parts){
    if(function_exists('is_shop')){
        if(is_shop())$parts['title']='Magazin';
        if(is_cart())$parts['title']='Coș';
        if(is_checkout())$parts['title']='Finalizare comandă';
        if(is_account_page())$parts['title']='Contul meu';
    }
    return $parts;
});
add_filter('the_title',function($title,$id){
    if(!is_admin() && function_exists('wc_get_page_id')) foreach(['shop'=>'Magazin','cart'=>'Coș','checkout'=>'Finalizare comandă','myaccount'=>'Contul meu'] as $key=>$label) if($id===wc_get_page_id($key))return $label;
    return $title;
},10,2);
add_filter('woocommerce_product_add_to_cart_description',function($description,$product){return $product->is_type('simple')?'Adaugă în coș: '.$product->get_name():$description;},10,2);
add_filter('gettext',function($translation,$original,$domain){
    if($domain==='woocommerce') return ['Shop order'=>'Sortarea produselor','Showing all %d results'=>'Sunt afișate toate cele %d produse','Showing the single result'=>'Este afișat un produs','Subtotal'=>'Subtotal','Product'=>'Produs'][$original]??$translation;
    return $translation;
},10,3);
add_filter('woocommerce_get_privacy_policy_text',function($text,$type){
    if((defined('CRPRINT_LOCAL_DEMO') && CRPRINT_LOCAL_DEMO) || str_starts_with($text,'Your personal data'))return $type==='registration'?'Folosim datele pentru administrarea contului. Detalii în [privacy_policy].':'Folosim datele pentru procesarea comenzii și comunicarea despre aceasta. Detalii în [privacy_policy].';
    return $text;
},10,2);
add_filter('woocommerce_privacy_policy_page_id',function($id){if(defined('CRPRINT_LOCAL_DEMO') && CRPRINT_LOCAL_DEMO){$ids=get_option('crprint_page_ids',[]);return $ids['confidentialitate']??$id;}return $id;});
add_filter('woocommerce_order_button_text',function($text){return defined('CRPRINT_LOCAL_DEMO') && CRPRINT_LOCAL_DEMO?'Plasează comanda':$text;});
add_filter('privacy_policy_url',function($url){
    if(defined('CRPRINT_LOCAL_DEMO') && CRPRINT_LOCAL_DEMO) return crprint_link('confidentialitate');
    return $url;
});
