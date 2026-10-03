<?php
// Used exclusively by the local Playground blueprint, never by production import.
require '/wordpress/wp-load.php';
update_option('blogname','CR Print 3D');
if(class_exists('WC_Install')) WC_Install::create_pages();
crprint_import_structure();
$ids=get_option('crprint_page_ids',[]);
foreach($ids as $key=>$id){
    $file=get_template_directory().'/layouts/'.$key.'.html';
    $post=['ID'=>$id,'post_status'=>'publish'];
    if(is_file($file)) $post['post_content']='<!-- wp:html -->'.file_get_contents($file).'<!-- /wp:html -->';
    wp_update_post($post);
}
update_option('show_on_front','page');
update_option('page_on_front',$ids['index']);
foreach(['nava-24-septembrie','nava-24-septembrie-digital'] as $sku){
    $id=wc_get_product_id_by_sku($sku);
    if($id){
        wp_update_post(['ID'=>$id,'post_status'=>'publish']);
        $p=wc_get_product($id);
        $digital=str_ends_with($sku,'-digital');
        $p->set_description($digital?'Model digital al navei „24 Septembrie”, în format FBX. Explorează geometria în previzualizarea 3D. Pentru detalii privind utilizarea modelului, contactează atelierul.':'Machetă navală printată 3D după modelul original al navei „24 Septembrie”. Pentru o scară, culoare sau finisare personalizată, discută cu atelierul înainte de comandă.');
        $p->set_short_description($digital?'Nava „24 Septembrie” în format digital FBX.':'Model naval din colecția CR Print 3D, disponibil ca machetă printată.');
        $p->save();
    }
}
foreach(['cart'=>'[woocommerce_cart]','checkout'=>'[woocommerce_checkout]'] as $key=>$content){
    $id=wc_get_page_id($key);
    if($id>0) wp_update_post(['ID'=>$id,'post_content'=>$content]);
}
foreach(['shop'=>'Magazin','cart'=>'Coș','checkout'=>'Finalizare comandă','myaccount'=>'Contul meu'] as $key=>$title){
    $id=wc_get_page_id($key);
    if($id>0) wp_update_post(['ID'=>$id,'post_title'=>$title]);
}
update_option('woocommerce_enable_guest_checkout','yes');
update_option('woocommerce_coming_soon','no');
update_option('woocommerce_store_pages_only','no');
update_option('woocommerce_bacs_settings',['enabled'=>'yes','title'=>'Comandă online','description'=>'Înregistrăm comanda și confirmăm detaliile înainte de pregătire.']);
update_option('woocommerce_cod_settings',['enabled'=>'no']);
update_option('woocommerce_cheque_settings',['enabled'=>'no']);
update_option('woocommerce_calc_taxes','no');
update_option('woocommerce_allowed_countries','specific');
update_option('woocommerce_specific_allowed_countries',['RO']);
update_option('woocommerce_ship_to_countries','specific');
update_option('woocommerce_specific_ship_to_countries',['RO']);
update_option('woocommerce_price_thousand_sep','.');
update_option('woocommerce_price_decimal_sep',',');
update_option('woocommerce_currency_pos','right_space');
if(!get_option('crprint_demo_shipping_zone')){
    $zone=new WC_Shipping_Zone();
    $zone->set_zone_name('România');
    $zone->set_zone_order(1);
    $zone->add_location('RO','country');
    $zone->save();
    $flat=$zone->add_shipping_method('flat_rate');
    update_option('woocommerce_flat_rate_'.$flat.'_settings',['title'=>'Curier','tax_status'=>'none','cost'=>'19']);
    $pickup=$zone->add_shipping_method('local_pickup');
    update_option('woocommerce_local_pickup_'.$pickup.'_settings',['title'=>'Ridicare în Constanța','tax_status'=>'none','cost'=>'0']);
    update_option('crprint_demo_shipping_zone',$zone->get_id());
}
$digital=wc_get_product(wc_get_product_id_by_sku('nava-24-septembrie-digital'));
if($digital && is_file(WP_CONTENT_DIR.'/uploads/woocommerce_uploads/nava-demo.zip')){
    $download=new WC_Product_Download();
    $download->set_id('crprint-local-demo');
    $download->set_name('NAVA 24 SEPTEMBRIE · FBX (ZIP)');
    $download->set_file(content_url('/uploads/woocommerce_uploads/nava-demo.zip'));
    $digital->set_downloads([$download]);
    $digital->set_download_limit(5);
    $digital->save();
}
update_option('woocommerce_file_download_method','force');
update_option('woocommerce_downloads_grant_access_after_payment','yes');
flush_rewrite_rules();

file_put_contents(ABSPATH.'.crprint-ready','CR Print local setup complete');
