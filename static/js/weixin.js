/*
 * 注意：
 * 1. 所有的JS接口只能在公众号绑定的域名下调用，公众号开发者需要先登录微信公众平台进入“公众号设置”的“功能设置”里填写“JS接口安全域名”。
 * 2. 如果发现在 Android 不能分享自定义内容，请到官网下载最新的包覆盖安装，Android 自定义分享接口需升级至 6.0.2.58 版本及以上。
 * 3. 完整 JS-SDK 文档地址：http://mp.weixin.qq.com/wiki/7/aaa137b55fb2e0456bf8dd9148dd613f.html
 *
 * 如有问题请通过以下渠道反馈：
 * 邮箱地址：weixin-open@qq.com
 * 邮件主题：【微信JS-SDK反馈】具体问题
 * 邮件内容说明：用简明的语言描述问题所在，并交代清楚遇到该问题的场景，可附上截屏图片，微信团队会尽快处理你的反馈。
 */
var voice = {
    localId: '',
    serverId: ''
};

function IsPC() {
        var userAgentInfo = navigator.userAgent;
        var Agents = ["Android", "iPhone",
                    "SymbianOS", "Windows Phone",
                    "iPad", "iPod"];
        var flag = true;
        for (var v = 0; v < Agents.length; v++) {
            if (userAgentInfo.indexOf(Agents[v]) > 0) {
                flag = false;
                break;
            }
        }
        return flag;
    }
    function IsIOS() {
        var userAgentInfo = navigator.userAgent;
        var Agents = ["iPhone", "iPad", "iPod"];
        var flag = false;
        for (var v = 0; v < Agents.length; v++) {
            if (userAgentInfo.indexOf(Agents[v]) > 0) {
                flag = true;
                break;
            }
        }
        //alert("IsIOS: " + flag + "; " + userAgentInfo);
        return flag;
    }

wx.ready(function () {
  /*
  var media = document.getElementById("musicBox");
  if (!media.src) {
      media.src = "http://h5.xf-yun.com/audioStream/941da7a3dc19399fae4df880b6fc59ac.mp3";
  }
  media.play();*/

  //window.xaudio.src = "";
  if (IsIOS())
  {
    load_auto_play();
    check_audio_url();  //此处非常重要，如果不在ready回调中直接设置audio的src，在IOS中是无法自动播放的
  }

/*
  wx.checkJsApi({
      jsApiList: ["checkJsApi"],
      success: function(res) {

        //alert("success before play");
        //load_auto_play();
        //alert("success after play");

        document.getElementById('bgmusic').src = "http://oj1hxt5z0.bkt.clouddn.com/123.mp3";
        document.getElementById('bgmusic').play();
      },
      error: function() {
        alert("error before play");
        load_auto_play();
        alert("error after play");
      }
    });
*/

  // 4.4 监听录音自动停止
  wx.onVoiceRecordEnd({
    complete: function (res) {
      voice.localId = res.localId;
      alert('录音时间已超过一分钟');
    }
  });

  // 4.8 监听录音播放停止
  wx.onVoicePlayEnd({
    complete: function (res) {
      alert('录音（' + res.localId + '）播放结束');
    }
  });

});

wx.error(function (res) {
  alert(res.errMsg);
});

