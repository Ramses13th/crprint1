<?php
/**
 * Plugin Name: CR Print Core
 * Description: Import sigur al paginilor, produse în ciornă și formular cu wp_mail pentru WP Mail SMTP.
 * Version: 2.0.0
 * Requires PHP: 8.2
 * License: GPL-2.0-or-later
 */
if(!defined('ABSPATH'))exit;
// The local Playground receives no SMTP credentials and must never send mail.
if(defined('CRPRINT_LOCAL_DEMO') && CRPRINT_LOCAL_DEMO){
    add_filter('pre_wp_mail',function(){return false;});
    // The local SQLite translator cannot execute Woo's MySQL stock-reservation query.
    // Normal stock validation/reduction remain active; production retains reservations.
    add_filter('woocommerce_hold_stock_for_checkout','__return_false');
}
add_action('init',function(){register_post_type('crprint_message',array('labels'=>array('name'=>'Solicitări 3D','singular_name'=>'Solicitare 3D'),'public'=>false,'show_ui'=>true,'show_in_rest'=>false,'menu_icon'=>'dashicons-email-alt','supports'=>array('title','editor'),'capabilities'=>array('edit_post'=>'manage_options','read_post'=>'manage_options','delete_post'=>'manage_options','edit_posts'=>'manage_options','edit_others_posts'=>'manage_options','publish_posts'=>'manage_options','read_private_posts'=>'manage_options','delete_posts'=>'manage_options'),'map_meta_cap'=>false));});
add_action('admin_menu',function(){add_management_page('CR Print — configurare','CR Print — configurare','manage_options','crprint-setup','crprint_setup_screen');});
function crprint_setup_screen(){
    if(!current_user_can('manage_options'))return;
    if(isset($_POST['crprint_import'])){check_admin_referer('crprint_setup');$result=crprint_import_structure();echo '<div class="notice notice-success"><p>'.esc_html($result).'</p></div>';}
    if(isset($_POST['crprint_settings'])){check_admin_referer('crprint_settings');$email=sanitize_email(wp_unslash($_POST['contact_email']??''));if(is_email($email))update_option('crprint_contact_email',$email);}
    echo '<div class="wrap"><h1>CR Print — configurare</h1><p>Activează tema CR Print Studio și WooCommerce, apoi creează structura. Paginile și produsele noi rămân în ciornă. Conținutul existent nu este suprascris.</p><form method="post">';wp_nonce_field('crprint_setup');submit_button('Creează pagini și produse în ciornă','primary','crprint_import');echo '</form><hr><h2>Email pentru solicitări</h2><form method="post">';wp_nonce_field('crprint_settings');echo '<input type="email" name="contact_email" value="'.esc_attr(get_option('crprint_contact_email','hi@crprint.ro')).'" required>';submit_button('Salvează destinatarul','secondary','crprint_settings');echo '</form><p>Configurează From Email și mailer-ul din WP Mail SMTP. Pluginul nostru folosește wp_mail; nu conține parole SMTP.</p><p>După verificare, publică paginile, alege pagina Acasă din Setări → Citire și confirmă prețurile produselor.</p></div>';
}
function crprint_product_image($filename){
    if(!in_array($filename,array('nava-studio.webp','nava-side.webp','nava-detail.webp'),true))return 0;
    $existing=get_posts(array('post_type'=>'attachment','post_status'=>'inherit','numberposts'=>1,'meta_key'=>'_crprint_asset','meta_value'=>$filename));
    if($existing)return $existing[0]->ID;
    $source=get_template_directory().'/assets/images/'.$filename;if(!is_file($source))return 0;
    $uploaded=wp_upload_bits($filename,null,file_get_contents($source));if(!empty($uploaded['error']))return 0;
    $id=wp_insert_attachment(array('post_mime_type'=>'image/webp','post_title'=>'Nava 24 Septembrie — randare','post_status'=>'inherit'),$uploaded['file']);
    if(is_wp_error($id)||!$id)return 0;
    require_once ABSPATH.'wp-admin/includes/image.php';wp_update_attachment_metadata($id,wp_generate_attachment_metadata($id,$uploaded['file']));
    update_post_meta($id,'_wp_attachment_image_alt','Randare din modelul original al navei 24 Septembrie');update_post_meta($id,'_crprint_asset',$filename);return $id;
}
function crprint_import_structure(){
    if(!function_exists('crprint_template_html'))return 'Activează întâi tema CR Print Studio.';
    $manifest=json_decode(file_get_contents(get_template_directory().'/layouts/pages.json'),true);$ids=get_option('crprint_page_ids',array());
    $titles=array('index'=>'Acasă','despre'=>'Atelier','servicii'=>'Servicii','portofoliu'=>'Portofoliu','contact'=>'Contact','modelare-3d'=>'Modelare 3D','printare-fdm'=>'Printare FDM','printare-sla'=>'Printare SLA','scanare-3d'=>'Scanare 3D','facescan'=>'FaceScan / BodyScan','confidentialitate'=>'Confidențialitate','termeni'=>'Termeni și condiții');
    foreach($titles as $key=>$title){
        if(!empty($ids[$key])&&get_post($ids[$key]))continue;
        $slug=$key==='index'?'crprint-acasa':$key;if(get_page_by_path($slug))$slug='crprint-'.$slug;
        $file=get_template_directory().'/layouts/'.$key.'.html';if(!is_file($file))continue;
        $content=file_get_contents($file);$id=wp_insert_post(array('post_type'=>'page','post_title'=>$title,'post_name'=>$slug,'post_status'=>'draft','post_content'=>'<!-- wp:html -->'.$content.'<!-- /wp:html -->'),true);
        if(!is_wp_error($id)){$ids[$key]=$id;update_post_meta($id,'_crprint_layout',$key);update_post_meta($id,'_crprint_description',$manifest[$key]['description']??'');}
    }
    update_option('crprint_page_ids',$ids);
    if(function_exists('wc_get_product_id_by_sku')){
        foreach(array(array('nava-24-septembrie','Nava · 24 Septembrie',149,false,'nava-studio.webp'),array('nava-24-septembrie-digital','Nava · fișier digital FBX',49,true,'nava-side.webp')) as $item){
            if(wc_get_product_id_by_sku($item[0]))continue;
            $p=new WC_Product_Simple();$p->set_name($item[1]);$p->set_sku($item[0]);$p->set_status('draft');$p->set_regular_price($item[2]);$p->set_virtual($item[3]);$p->set_downloadable($item[3]);$p->set_description('Produs exemplu. Înainte de publicare: confirmă prețul real, scara, materialul, finisajul și licența. Prețul importat este demonstrativ.');$p->set_short_description($item[3]?'Model digital FBX. Configurează fișierul protejat și licența înainte de publicare.':'Machetă navală printată 3D. Configurează dimensiunile și materialul înainte de publicare.');$p->set_manage_stock(!$item[3]);if(!$item[3])$p->set_stock_quantity(20);$p->save();
            $main=crprint_product_image($item[4]);$p->set_image_id($main);
            $gallery=array();foreach(array('nava-studio.webp','nava-side.webp','nava-detail.webp') as $image){if($image!==$item[4]){$id=crprint_product_image($image);if($id)$gallery[]=$id;}}
            $p->set_gallery_image_ids($gallery);
            $term=term_exists('colectia-navala','product_cat');if(!$term)$term=wp_insert_term('Colecția navală','product_cat',array('slug'=>'colectia-navala'));
            if(!is_wp_error($term))$p->set_category_ids(array(intval($term['term_id'])));$p->save();
        }
    }
    if(!has_nav_menu('primary')){$menu=wp_create_nav_menu('CR Print principal');if(!is_wp_error($menu)){$items=array('index','despre','servicii','portofoliu','magazin','contact');foreach($items as $key){$url=crprint_link($key);wp_update_nav_menu_item($menu,0,array('menu-item-title'=>$key==='magazin'?'Magazin':($titles[$key]??$key),'menu-item-url'=>$url,'menu-item-status'=>'publish','menu-item-type'=>'custom'));}$locations=get_theme_mod('nav_menu_locations',array());$locations['primary']=$menu;set_theme_mod('nav_menu_locations',$locations);}}
    return 'Structură creată în ciornă. Produsele și paginile existente au fost păstrate. Publică numai după verificare și configurează pagina Acasă din Setări → Citire.';
}
add_shortcode('crprint_contact_form',function(){
    if(!function_exists('crprint_template_html'))return 'Formularul necesită tema CR Print Studio.';
    $a=wp_rand(2,8);$b=wp_rand(1,5);$id=wp_generate_uuid4();set_transient('crprint_ch_'.$id,array('answer'=>$a+$b,'created'=>time()),30*MINUTE_IN_SECONDS);
    $form=crprint_template_html('contact-form');
    $form=preg_replace('/<form([^>]*)>/','<form$1 action="'.esc_url(admin_url('admin-post.php')).'" method="post">',$form,1);
    $hidden='<input type="hidden" name="action" value="crprint_contact"><input type="hidden" name="challenge_id" value="'.esc_attr($id).'">'.wp_nonce_field('crprint_contact','crprint_nonce',true,false);
    $form=str_replace('</form>',$hidden.'</form>',$form);
    $form=str_replace('se încarcă…',$a.' + '.$b,$form);
    $form=str_replace('În demo, mesajul este salvat local și apare în administrare. Emailul real se activează în WordPress.','Solicitarea ajunge la echipa CR Print 3D. Îți răspundem pe email sau telefon, în timpul programului.',$form);
    $notices=array('received'=>'Solicitarea a fost înregistrată. Îți răspundem în timpul programului.','saved'=>'Solicitarea a fost înregistrată. Îți răspundem în timpul programului.','invalid'=>'Verifică datele, acordul și noul calcul anti-spam.','limited'=>'Ai trimis mai multe solicitări. Așteaptă câteva minute sau sună-ne.','unavailable'=>'Solicitarea nu a putut fi înregistrată. Scrie-ne la hi@crprint.ro sau sună la 0735 961 151.');
    $state=sanitize_key($_GET['contact_status']??'');
    $reference=sanitize_key($_GET['contact_ref']??'');
    $verified=in_array($state,array('received','saved'),true) && $reference && get_transient('crprint_receipt_'.$reference);
    $tracking=$verified?' data-contact-reference="'.esc_attr($reference).'"':'';
    $notice=isset($notices[$state])?'<div class="demo-banner" role="status"'.$tracking.'><p>'.esc_html($notices[$state]).'</p></div>':'';
    return $notice.$form;
});
add_action('admin_post_nopriv_crprint_contact','crprint_handle_contact');add_action('admin_post_crprint_contact','crprint_handle_contact');
function crprint_handle_contact(){
    $back=function($status,$reference=''){$url=function_exists('crprint_link')?crprint_link('contact'):home_url('/contact/');$args=array('contact_status'=>$status);if($reference)$args['contact_ref']=$reference;wp_safe_redirect(add_query_arg($args,$url).'#contact-form');exit;};
    if(!isset($_POST['crprint_nonce'])||!wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['crprint_nonce'])),'crprint_contact'))$back('invalid');
    $challenge_id=sanitize_text_field(wp_unslash($_POST['challenge_id']??''));$challenge=get_transient('crprint_ch_'.$challenge_id);
    if(!empty($_POST['company_website'])||!$challenge||time()-$challenge['created']<1||!isset($_POST['answer'])||intval($_POST['answer'])!==$challenge['answer']||empty($_POST['consent']))$back('invalid');
    delete_transient('crprint_ch_'.$challenge_id);
    $rate_key='crprint_rate_'.hash_hmac('sha256',$_SERVER['REMOTE_ADDR']??'local',wp_salt());$rate=intval(get_transient($rate_key));if($rate>=6)$back('limited');set_transient($rate_key,$rate+1,10*MINUTE_IN_SECONDS);
    $name=mb_substr(sanitize_text_field(wp_unslash($_POST['name']??'')),0,100);$email=sanitize_email(wp_unslash($_POST['email']??''));$phone=mb_substr(sanitize_text_field(wp_unslash($_POST['phone']??'')),0,40);$service=mb_substr(sanitize_text_field(wp_unslash($_POST['service']??'')),0,100);$message=mb_substr(sanitize_textarea_field(wp_unslash($_POST['message']??'')),0,5000);
    if(mb_strlen($name)<2||!is_email($email)||mb_strlen($message)<10)$back('invalid');
    $body="Nume: $name\nEmail: $email\nTelefon: $phone\nServiciu: $service\n\n$message";
    $record=wp_insert_post(array('post_type'=>'crprint_message','post_status'=>'private','post_title'=>'Solicitare — '.$name.' — '.current_time('Y-m-d H:i'),'post_content'=>$body),true);
    if(is_wp_error($record))$back('unavailable');
    $recipient=get_option('crprint_contact_email','hi@crprint.ro');$sent=wp_mail($recipient,'Solicitare nouă CR Print 3D',$body,array('Content-Type: text/plain; charset=UTF-8','Reply-To: '.$email));
    if(!is_wp_error($record))update_post_meta($record,'_crprint_email_accepted',$sent?'yes':'no');
    $reference=wp_generate_uuid4();set_transient('crprint_receipt_'.$reference,true,10*MINUTE_IN_SECONDS);
    $back($sent?'received':'saved',$reference);
}
// Complete only the seeded local examples; existing custom galleries are preserved.
add_action('admin_init',function(){
    if(!defined('CRPRINT_LOCAL_DEMO')||!CRPRINT_LOCAL_DEMO||!function_exists('wc_get_product_id_by_sku'))return;
    foreach(array('nava-24-septembrie','nava-24-septembrie-digital') as $sku){
        $p=wc_get_product(wc_get_product_id_by_sku($sku));if(!$p||$p->get_gallery_image_ids())continue;
        $main=str_ends_with($sku,'-digital')?'nava-side.webp':'nava-studio.webp';$gallery=array();
        foreach(array('nava-studio.webp','nava-side.webp','nava-detail.webp') as $file){if($file!==$main){$id=crprint_product_image($file);if($id)$gallery[]=$id;}}
        $p->set_gallery_image_ids($gallery);$term=term_exists('colectia-navala','product_cat');if(!$term)$term=wp_insert_term('Colecția navală','product_cat',array('slug'=>'colectia-navala'));if(!is_wp_error($term))$p->set_category_ids(array(intval($term['term_id'])));$p->save();
    }
});
