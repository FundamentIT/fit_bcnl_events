odoo.define('fit_bcnl_events.website.snippets.animation', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var base = require('web_editor.base');
    var animation = require('web_editor.snippets.animation');
    var web_animation = require('website.snippets.animation');

    var qweb = core.qweb;
    // Opera 8.0+
    var isOpera = (!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;
    // Firefox 1.0+
    var isFirefox = typeof InstallTrigger !== 'undefined';
    // Safari 3.0+ "[object HTMLElementConstructor]"
    var isSafari = /constructor/i.test(window.HTMLElement) || (function (p) { return p.toString() === "[object SafariRemoteNotification]"; })(!window['safari'] || (typeof safari !== 'undefined' && safari.pushNotification));
    // Internet Explorer 6-11
    var isIE = /*@cc_on!@*/false || !!document.documentMode;
    // Edge 20+
    var isEdge = !isIE && !!window.StyleMedia;
    // Chrome 1+
    var isChrome = !!window.chrome && !!window.chrome.webstore;
    // Blink engine detection
    var isBlink = (isChrome || isOpera) && !!window.CSS;

    animation.registry.parallax = animation.registry.parallax.extend({

         on_scroll: function () {
            if (this.speed === 1) return;
            var top = this.offset + $(document).scrollTop() * this.speed;
            //var top = this.offset + window.scrollY * this.speed;
            if (isIE || isEdge) {
                //console.log('NNNEEEEEEEEE!!!!');
            } else {
                //this.$target.css("background-position", "0px " + top + "px");
                this.$target.css("background-position", "0px " + top + "px");
            }
        },
    });

});