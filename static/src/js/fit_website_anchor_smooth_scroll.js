/**
*    Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
*    Copyright 2016 LasLabs Inc.
*    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
**/

odoo.define('website_anchor_smooth_scroll', function(require) {
    'use strict';

    var base = require('web_editor.base');

    var smooth_scroll = function(event) {
        //event.preventDefault();
        var anchor_fragment = event.target.hash;
        //check for span in a href
        if (typeof anchor_fragment == 'undefined') {
            anchor_fragment = event.target.parentNode.hash;
        }
        // Do this before scrolling so that browser history accurately reflects scroll position at time of click
        history.pushState(null, document.title, anchor_fragment);
        var offset = $(anchor_fragment).offset();
        var scrollTop = $(anchor_fragment).offset().top - 100;
        return $('html, body').stop().animate({
                'scrollTop': scrollTop
        }).promise();
    };

    var hide_smooth_scroll_links = function(event) {
        console.log('FIT hide_smooth_scroll_links');
        $('ul[class*="navbar-right"] li a[href^="#"][href!="#"][href!="#advanced-view-editor"]').each(function(index) {
            $(this).fadeOut(500, function() {
                $(this).css('display','none');
            });
        });
    };

    var show_smooth_scroll_links = function(event) {
        console.log('FIT show_smooth_scroll_links');
        $('ul[class*="navbar-right"] li a[href^="#"][href!="#"][href!="#advanced-view-editor"]').each(function(index) {
            $(this).fadeIn(500, function() {
                $(this).css('display','block');
            });
        });

    };

    jQuery(document).ready(function() {
        var location = $(window.location).attr('pathname');
        if (location == '/event' || location == '/page/contactus'){
            hide_smooth_scroll_links();
        }
        else {
            show_smooth_scroll_links();
        }
    });

    base.ready().done(function() {
        $('a[href^="#"][href!="#"][href!="#advanced-view-editor"]').click(smooth_scroll);
        //$('a[href~="/event"]').click(hide_smooth_scroll_links);
        //$('a[href="/"]').click(show_smooth_scroll_links);
        //$('a[href^="#"][href!="#"][href!="#advanced-view-editor"]').click(smooth_scroll);
    });

    return {'scroll_handler': smooth_scroll};
});
