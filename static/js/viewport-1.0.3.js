/*
* Viewport v1.0.3
* Copyright 2013 - 2014, Micky
* Dual licensed under the MIT License
* 2014-05-13
*/
(function(doc){
	var script = doc.getElementsByTagName("script"),
		me = script[script.length - 1],
		ua = navigator.userAgent,
		originalViewport = doc.querySelector("meta[name=viewport]"),
		viewport = (function(width){
		var v = doc.createElement("meta");
		v.setAttribute("name", "viewport");
		v.setAttribute("content", "width=" + (!/ip(?=od|ad|hone)/i.test(ua) && /MicroMessenger/.test(ua) ? "device-width,target-densitydpi=" + (width / screen.width * devicePixelRatio * 160) : width) + ",user-scalable=no");
		return v;
	})(me.dataset.width || 640);
	originalViewport && doc.head.removeChild(originalViewport);
	doc.head.appendChild(viewport);
	me.parentNode.removeChild(me);
})(document);
