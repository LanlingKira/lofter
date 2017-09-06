// ==UserScript==
// @name         Lofter(乐乎)原图查看下载
// @namespace    LofterSpider
// @version      0.1.1
// @description  下载lofter上的超清原图，prprprpr
// @author       兰陵
// @match        http*://*.lofter.com/post/*
// @run-at       document-end
// @grant        GM_xmlhttpRequest
// @connect      *
// ==/UserScript==
(function() {
    "use strict";
    var css = document.createElement("style");
    css.type = "text/css";
    css.id = "spidercss";
    var cssText = "#lofterspider{position:fixed;top:0;left:50%;width:100%;height:100%;background:rgba(229,229,229,.95);padding:0;margin:0 auto;font-size:16px;-webkit-transform:translateX(-50%);transform:translateX(-50%);z-index:9999999999999}#lofterspider p:first-child{position:absolute;left:0;top:0;width:100%;padding:10px;background:#fff;box-shadow:0 0 4px rgba(0,0,0,.2);text-align:center;font-size:1.5em;color:#555}#spiderclose{position:absolute;right:12px;padding:10px 0 10px 16px;font-size:1.5em;border-left:1px solid #555;font-weight:700;color:#555}#lofterspider ul{position:relative;top:15%}#lofterspider ul li{width:20%;text-align:center;float:left;padding-bottom:5px}#lofterspider ul li img{width:90%}#lofterspider ul li img:hover{opacity:.6}#lofterspider ul li p{color:#555}#lofterspider ul li p a{margin:auto 10px;color:#673ab7}#spiderboprt{position:fixed;top:7px;right:15px;margin:0 5px 0 0}#spiderboprt a,#spiderboprt em{height:23px;line-height:23px;float:left;background:url(//l.bst.126.net/rsc/img/control/operatenew24.png?005) no-repeat}#spiderboprt a{padding:0 2px 0 0;cursor:pointer;text-decoration:none;background-position:right 0}#spiderboprt a:hover em,#spiderboprt em{color:#fff;padding:0 5px 0 26px;white-space:nowrap;font-weight:400;font-style:normal}#spiderboprt em{background-position:0 -750px}#spiderboprt a:hover em{background-position:0 -780px}";
    css.innerHTML = cssText;
    if (document.getElementById("spidercss") == undefined) {
        document.getElementsByTagName("head")[0].appendChild(css);
    }
    if (document.getElementById("spiderboprt") == undefined) {
        var Scope = document.getElementById("control_frame");
        Scope.style.right = "77px";
        var boprt = document.createElement("div");
        boprt.id = "spiderboprt";
        Scope.parentNode.insertBefore(boprt, Scope.nextSibling);
        document.getElementById("spiderboprt").innerHTML = "<a><em>下载</em></a>";
    }
    var i, j = document.getElementsByClassName("imgclasstag").length, preg = /(.*?)\.(jpg|png|jpeg|gif)/i, k = "";
    for (i = 0; j > i; i++) {
        var imgurl = document.getElementsByClassName("imgclasstag")[i].getAttribute("bigimgsrc").match(preg)[0];
        var ext = imgurl.match(/\.(jpg|png|jpeg|gif)/i)[0];
        k += '<li><img src="' + imgurl + '?imageView&thumbnail=350y350&enlarge=1&quality=90&type=jpg"><p>' + (i + 1) + '.<a href="' + imgurl + '" target="_blank">查看原图</a><a href="' + imgurl + '" download="' + document.title + " - " + document.location.pathname.substring(6) + "[" + (i + 1) + "]" + ext + '">下载原图</a></p></li>';
    }
    function Append(k) {
        var pElement = document.createElement("div");
        pElement.id = "lofterspider";
        document.body.appendChild(pElement);
        var LofterSpider = document.getElementById("lofterspider");
        LofterSpider.innerHTML = "<p>" + document.title + '</p><p id="spiderclose">X</p><ul>' + k + '</ul><p style="position:fixed;bottom:0;right:10px;color:#555"><i>请遵守作品协议</i></p>';
        document.getElementsByTagName("body")[0].style.overflow = "hidden";
    }
    function Close() {
        var LofterSpider = document.getElementById("lofterspider");
        LofterSpider.parentNode.removeChild(LofterSpider);
        document.getElementsByTagName("body")[0].style.overflow = "";
    }
    function Download(a) {
        var oldhtml = a.innerHTML;
        GM_xmlhttpRequest({
            method:"GET",
            url:a.href,
            responseType:"blob",
            overrideMimeType:"text/plain; charset=x-user-defined",
            onprogress:function(xhr) {
                if (xhr.lengthComputable) {
                    a.innerHTML = (xhr.loaded / xhr.total * 100).toFixed(2) + "%";
                }
            },
            onload:function(xhr) {
                if (this.readyState == 4 && this.status == 200) {
                    var blob = this.response;
                    saveFile(blob, a.download);
                    a.innerHTML = oldhtml;
                    a.isDownload = false;
                }
            }
        });
    }
    function saveFile(blob, filename) {
        if (window.navigator.msSaveBlob) {
            window.navigator.msSaveBlob(blob, filename);
        } else {
            var a = document.createElement("a");
            var url = URL.createObjectURL(blob);
            a.href = url;
            a.download = filename;
            var evt = document.createEvent("MouseEvents");
            evt.initEvent("click", true, true);
            a.dispatchEvent(evt);
            URL.revokeObjectURL(url);
        }
    }
    function Lofter() {
        Append(k);
        var ars = document.querySelectorAll("a[href][download]");
        for (var l = 0; l < ars.length; l++) {
            var a = ars[l];
            a.addEventListener("click", function(e) {
                e.preventDefault();
                if (!this.isDownload) Download(this);
                this.isDownload = true;
                return false;
            }, true);
        }
        document.getElementById("spiderclose").onclick = function() {
            Close();
        };
    }
    document.getElementById("spiderboprt").onclick = function() {
        Lofter();
    };
    document.onkeydown = function() {
        if (document.getElementById("lofterspider") != undefined && event.keyCode == 27) {
            Close();
        }
    };
})();
