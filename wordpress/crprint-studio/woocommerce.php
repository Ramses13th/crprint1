<?php
if(!defined('ABSPATH'))exit;get_header();echo '<section class="section"><div class="container woocommerce">';
if(is_shop())echo '<div class="section-heading"><div><p class="eyebrow">DIN ATELIERUL CR PRINT 3D</p><h1>Obiecte cu poveste.</h1><p>Machete printate și modele digitale. Alege ce îți place, în forma potrivită.</p></div></div>';
woocommerce_content();echo '</div></section>';get_footer();
