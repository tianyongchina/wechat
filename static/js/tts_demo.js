/*

 */

/***********************************************local Variables**********************************************************/
var audioPlayUrl = "http://h5.xf-yun.com/audioStream/";

/**
  * 初始化Session会话
  * url                 连接的服务器地址（可选）
  * reconnection        客户端是否支持断开重连
  * reconnectionDelay   重连支持的延迟时间   
  */
var session = new IFlyTtsSession({
									'url'                : 'ws://h5.xf-yun.com/tts.do',
									'reconnection'       : true,
									'reconnectionDelay'  : 30000
								});
/* 音频播放对象 */
window.xaudio = null;
/* 音频播放状态 0:未播放且等待音频数据状态，1:正播放且等待音频数据状态，2：未播放且不等待音频数据*/
var audio_state = 0;
var audio_vcn = "xiaoyu";//"aisxping";//"xiaofeng";//"xiaoyan";
/*
var audio_speed = 25;
var audio_speed_max = 50;
var audio_volume = 25;
var audio_volume_max = 50;
*/
/*
设置 volume 属性：
audio|video.volume=volumevalue
返回 volume 属性：
audio|video.volume
属性值
值	描述
volumevalue
规定音频/视频的当前音量。必须是介于 0.0 与 1.0 之间的数字。
例值：
1.0 是最高音量（默认）
0.5 是一半音量 （50%）
0.0 是静音

设置 playbackRate 属性：
audio|video.playbackRate=playbackspeed
返回 playbackRate 属性：
audio|video.playbackRate
属性值
值	描述
playbackspeed
指示音频/视频的当前播放速度。
例值：
1.0 正常速度
0.5 半速（更慢）
2.0 倍速（更快）
-1.0 向后，正常速度
-0.5 向后，半速
*/
var audio_speed = 0.5;
var audio_speed_max = 4;
var audio_volume = 0.5;
var audio_volume_max = 1;

var audio_list = new Array();
var audio_play_index = -1;
var audio_text_all = new Array();
var audio_text_subjects = new Array();
var is_play_subject = true;
/*播放被打断时的状态*/
var audio_break_src = "";
var audio_break_currentTime = -1;

var reading_color = "#DC4700";
var notread_color = "#5a5a5a";

/***********************************************local Variables**********************************************************/
/**
  * 停止播放音频
  *
  */
function stop() {
    audio_state = 2;
    window.xaudio.pause();
}

function start() {
	audio_state = 1;
	window.xaudio.play();
}

/**
  * 重置音频缓存队列和播放对象
  * 若音频正在播放，则暂停当前播放对象，创建并使用新的播放对象.
  */
function reset()
{
	audio_state = 0;
	if(window.xaudio != null)
	{
		window.xaudio.pause();
	}
	else
	{
		window.xaudio = new Audio();
		window.xaudio.addEventListener('ended', cb_audio_play_end, false);
	}
	
	//alert("reset()0.............audio_url: "+ window.xaudio.src);
	//window.xaudio = new Audio();//IOS有问题，不能播放第二个
	//window.xaudio = document.getElementById('xaudio');
	window.xaudio.src = "";
	//alert("reset()1.............audio_url: "+ window.xaudio.src);
}

function get_play_state()
{
	return audio_state;
}

function play(content, vcn) {
	reset();

	//设置正在播报的文字颜色为红色
	changeTextColor(audio_play_index, reading_color);

	//alert("reset()2.............audio_url: "+ window.xaudio.src);
	//自动滚动到播放的位置
	ScrollToIndex(audio_play_index);

	//"params": "ent=aisound,aue=lame,vcn=" + vcn + ",spd=" + audio_speed + ",vol=" + audio_volume
	ssb_param = {
		"appid": '58b547ae',
		"appkey": "0a4b462814a5bb55",
		"synid": "12345",
		"params": "ent=aisound,aue=lame,vcn=" + vcn
	};

	//console.log("audio play start :" + content);
	//alert("0");
	session.start(ssb_param, content, function (err, obj) {
		var audio_url = audioPlayUrl + obj.audio_url;
		if (audio_url != null && audio_url != undefined) {
			//alert("1");
			window.xaudio.src = audio_url;
            //window.xaudio.src = "./8400.mp3";
            //window.xaudio.preload = "auto";
            //window.xaudio.autoplay = "autoplay";
			//console.log("window.xaudio.play().............audio_url: "+ audio_url);
			//alert("2");
			window.xaudio.load();
			//alert("3");
			window.xaudio.play();
			//alert("4");
		}
	}, function (message) {
		if (message == 'onStop') {
			console.log("onStop.............");
			//alert("onStop.............");
		}
		else if (message == 'onEnd') {
			console.log("onEnd.............");
			//alert("onEnd.............");
		}
	});
}

function playBySrcAndcurrentTime(src, currentTime) {
	reset();

	if (src != "" && currentTime != -1)
	{
		window.xaudio.src = src;
		window.xaudio.load();
		window.xaudio.play();
		//alert("playBySrcAndcurrentTime: " + audio_break_currentTime);
		window.xaudio.currentTime = audio_break_currentTime;
	}
}

function check_audio_url()
{
	var i = 0;
	//while (window.xaudio == null || window.xaudio.src.indexOf(audioPlayUrl) < 0)
	while (window.xaudio == null || window.xaudio.src == "")
	{
		i++;
	}

	window.xaudio.src = window.xaudio.src;
	window.xaudio.play();
	//alert("check_audio_url after window.xaudio.play().............audio_url: "+ window.xaudio.src);
}


/**
  * 播放语音列表：实际上只是从第一个开始播放。需要通过回调返回的信息，确定播放完成之后，再去播放下一句
  *
  */

function play_subject_list() {
	audio_list = audio_text_subjects.concat();
	is_play_subject = true;
	playlist();
}

function play_all_list() {
	audio_list = audio_text_all.concat();
	is_play_subject = false;
	playlist();
}

function playlist() {
	audio_play_index = 0;
	play(audio_list[audio_play_index], audio_vcn);
}

function cb_audio_play_end() {
	if (audio_break_currentTime != -1)
	{
		//有被打断的播放音频，此时src还在有效期内
		playBySrcAndcurrentTime(audio_break_src, audio_break_currentTime);
		audio_break_currentTime = -1;
		audio_break_src = "";
	}
	else
	{
		//设置播报完成的文字颜色为黑色
		changeTextColor(audio_play_index, notread_color);

		audio_play_index++;
		//alert("audio_play_index="+audio_play_index+" listlength="+audio_list.length);
		if (audio_play_index < audio_list.length) {
			play(audio_list[audio_play_index], audio_vcn);
		}
		else {
			console.log("audio play over......................");
			audio_play_index = audio_list.length;
		}
	}
}

function getIdByIndex(play_index) {
	var id;
	if (play_index == 0)
	{
		id = "titleinfo";
	}
	else
	{
		if (is_play_subject)
		{
			id = "subject_no_" + play_index;
		}
		else
		{
			id = "all_no_" + play_index;
		}
	}
	return id;
}

function changeTextColor(play_index, color) {
	var textobj =  document.getElementById(getIdByIndex(play_index));
	if (textobj)
	{
		textobj.style.color = color;
	}
}

function ScrollToIndex(play_index)
{
	if (IsIOS())
		return;

	var textobj =  document.getElementById(getIdByIndex(play_index));
	if (textobj) {/*
	 $('html, body').animate({
	 scrollTop: textobj.style.top
	 }, 1000);*/
		var offsetTopTmp = textobj.offsetTop;
		if (offsetTopTmp > 150) {
			offsetTopTmp = offsetTopTmp - 150;
			$('html, body').scrollTop(offsetTopTmp);
			//$('content_show').scrollTop(offsetTopTmp);
		}
	}
}

function setXSpeed(speedValue)
{
	window.xaudio.defaultPlaybackRate = speedValue;
	window.xaudio.playbackRate = speedValue;
}

function setXVolume(volumeValue)
{
	window.xaudio.volume = volumeValue;
}

function isContains(str, substr) {
    return str.indexOf(substr) >= 0;
}

function playcontrol_bak(con) {
	var bControl = false;	//需要重新播放
	var bChangeColor = false;	//需要改变颜色
	var oldIndex = audio_play_index;
    var flag  = true;
	/*
	if (isContains(con, '上一段') || isContains(con, '前一段') || isContains(con, '上一句') || isContains(con, '前一句') || isContains(con, '上一个') || isContains(con, '前一个')
	|| isContains(con, '上面的') || isContains(con, '前面的') || isContains(con, 'before') || isContains(con,'up'))
	{
		bChangeColor = true;
		bControl = true;
		audio_play_index--;
		if (audio_play_index < 0)
			audio_play_index = 0;
	}
	else if (isContains(con, '下一段') || isContains(con, '后一段') || isContains(con, '下一句') || isContains(con, '后一句') || isContains(con, '下一个') || isContains(con, '后一个')
	|| isContains(con, '下面的') || isContains(con, '后面的') || isContains(con, 'next') || isContains(con,'follow'))
	{
		bChangeColor = true;
		bControl = true;
		audio_play_index++;
		if (audio_play_index >= audio_list.length)
			audio_play_index = audio_list.length - 1;
	}*/
	if (isContains(con, '上一') || isContains(con, '前一') || isContains(con, '上面') || isContains(con, '前面')
		|| isContains(con, 'previous') || isContains(con,'up'))
	{
		bChangeColor = true;
		bControl = true;
		audio_play_index--;
		if (audio_play_index < 0)
			audio_play_index = 0;
	}
	else if (isContains(con, '下一') || isContains(con, '后一') || isContains(con, '下面') || isContains(con, '后面')
		|| isContains(con, 'next') || isContains(con,'down'))
	{
		bChangeColor = true;
		bControl = true;
		audio_play_index++;
		if (audio_play_index >= audio_list.length)
			audio_play_index = audio_list.length - 1;
	}
	else if (isContains(con, '重复') || isContains(con, 'repeat'))
	{
		bControl = true;
	}
	else if (isContains(con, '停止') || isContains(con, '不听了') || isContains(con, 'stop'))
	{
		//设置刚才播报的文字颜色为黑色
		changeTextColor(oldIndex, notread_color);
		bControl = true;
		stop();
		return;
	}
	else if (isContains(con, '继续') || isContains(con, '接着') || isContains(con, 'continue'))
	{
		bControl = true;
	}
	else if (isContains(con, '从头来') || isContains(con, '重新') || isContains(con, 'begin'))
	{
		bChangeColor = true;
		bControl = true;
		audio_play_index = 0;
	}
	else if (isContains(con, '快点') || isContains(con, '快一点') || isContains(con, '太慢了') || isContains(con, 'fast'))
	{
		//bControl = true;
		audio_speed += 0.5;//10;
		if (audio_speed > audio_speed_max)
			audio_speed = audio_speed_max;

		setXSpeed(audio_speed);
		return true;
	}
	else if (isContains(con, '慢点') || isContains(con, '慢一点') || isContains(con, '太快了') || isContains(con, 'slow'))
	{
		//bControl = true;
		audio_speed -= 0.5;//10;
		if (audio_speed < 0.5)
			audio_speed = 0.5;

		setXSpeed(audio_speed);
		return true;
	}
	else if (isContains(con, '大点声') || isContains(con, '大一点') || isContains(con, '听不见') || isContains(con, '声音太小了') || isContains(con, 'upper'))
	{
		//bControl = true;
		audio_volume += 0.1;//10;
		if (audio_volume > audio_volume_max)
			audio_volume = audio_volume_max;

		setXVolume(audio_volume);
		return true;
	}
	else if (isContains(con, '小点声') || isContains(con, '小一点') || isContains(con, '太吵了') || isContains(con, '声音太大了') || isContains(con, 'lower'))
	{
		//bControl = true;
		audio_volume -= 0.1;//10;
		if (audio_volume < 0.1)
			audio_volume = 0.1;

		setXVolume(audio_volume);
		return true;
	}
	else if (isContains(con, '摘要') || isContains(con, '简介') || isContains(con, '主题') || isContains(con, '概要') || isContains(con, '简单点') || isContains(con, '太多了') || isContains(con, 'summary') || isContains(con, 'outline') || isContains(con, 'simple'))
	{
		if (!is_play_subject)
		{
			stop();
			//设置刚才播报的文字颜色为黑色
			changeTextColor(oldIndex, notread_color);

			audio_list = audio_text_subjects.concat();
			is_play_subject = true;
			audio_play_index = 0;
			bControl = true;

			document.getElementById("all_div").style.display="none";//隐藏
			document.getElementById("subject_div").style.display="";//显示
		}
	}
	else if (isContains(con, '所有') || isContains(con, '全部') || isContains(con, '全文') || isContains(con, '详细点') || isContains(con, 'all') || isContains(con, 'full'))
	{
		if (is_play_subject)
		{
			stop();
			//设置刚才播报的文字颜色为黑色
			changeTextColor(oldIndex, notread_color);

			audio_list = audio_text_all.concat();
			is_play_subject = false;
			audio_play_index = 0;
			bControl = true;

			document.getElementById("subject_div").style.display="none";//隐藏
			document.getElementById("all_div").style.display="";//显示
		}
	} else {
        flag = false;    
    }
    

	if (bChangeColor)
	{
		//设置刚才播报的文字颜色为黑色
		changeTextColor(oldIndex, notread_color);
	}

	if (bControl)
		play(audio_list[audio_play_index], audio_vcn);
    return flag;
}

function playcontrol(con) {
	var bControl = false;	//需要重新播放
	var bChangeColor = false;	//需要改变颜色
	var oldIndex = audio_play_index;
    var flag  = true;
	
    if(con['domain'] == "speech") {
        if(con['param']['action'] == "speech_order") {
            var tmp_step = con['param']['step'];
            if(con['param']['direction'] == 'previous' && con['param']['quantity'] == "paragraph") {//向上读一段
                bChangeColor = true;
                bControl = true;
                audio_play_index -= tmp_step;
                if (audio_play_index < 0)
                    audio_play_index = 0;
            
            } else if(con['param']['direction'] == 'next' && con['param']['quantity'] == "paragraph") {//向下读一段
                bChangeColor = true;
                bControl = true;
                audio_play_index += tmp_step;
                if (audio_play_index >= audio_list.length)
                    audio_play_index = audio_list.length - 1;
            } else if(con['param']['quantity'] == "again") {
                bChangeColor = true;
                bControl = true;
                audio_play_index = 0;
            }
        //} else if(con['action'] == "stop") {
        } else if(con['param']['action'] == "pause" || con['param']['action'] == "stop") {
            //设置刚才播报的文字颜色为黑色
            changeTextColor(oldIndex, notread_color);
            bControl = true;
            stop();
            return;
        } else if(con['param']['action'] == "resume") {
            bControl = true;
        } else if(con['param']['action'] == "speech_speed_up") {
            //bControl = true;
            audio_speed += 0.5;//10;
            if (audio_speed > audio_speed_max)
                audio_speed = audio_speed_max;

            setXSpeed(audio_speed);
            return true;
        } else if(con['param']['action'] == "speech_speed_down") {
            //bControl = true;
            audio_speed -= 0.5;//10;
            if (audio_speed < 0.5)
                audio_speed = 0.5;

            setXSpeed(audio_speed);
            return true;
        } else if(con['param']['action'] == "speech_brief_mode") {
            if (!is_play_subject) {
                stop();
                //设置刚才播报的文字颜色为黑色
                changeTextColor(oldIndex, notread_color);

                audio_list = audio_text_subjects.concat();
                is_play_subject = true;
                audio_play_index = 0;
                bControl = true;

                document.getElementById("all_div").style.display="none";//隐藏
                document.getElementById("subject_div").style.display="";//显示
            }
        } else if(con['param']['action'] == "speech_all_mode") {
            if (is_play_subject) {
                stop();
                //设置刚才播报的文字颜色为黑色
                changeTextColor(oldIndex, notread_color);

                audio_list = audio_text_all.concat();
                is_play_subject = false;
                audio_play_index = 0;
                bControl = true;

                document.getElementById("subject_div").style.display="none";//隐藏
                document.getElementById("all_div").style.display="";//显示
            }
        }
    } else if(con['domain'] == "valume") {
        if(con['param']['action'] == "volume_down") {
            //bControl = true;
            audio_volume -= 0.1;//10;
            if (audio_volume < 0.1)
                audio_volume = 0.1;

            setXVolume(audio_volume);
            return true;

        } else if(con['param']['action'] == "volume_up") {
        
            //bControl = true;
            audio_volume += 0.1;//10;
            if (audio_volume > audio_volume_max)
                audio_volume = audio_volume_max;

            setXVolume(audio_volume);
            return true;
        }
    } else {
         flag = false;    
    }
    

	if (bChangeColor) {
		//设置刚才播报的文字颜色为黑色
		changeTextColor(oldIndex, notread_color);
	}

	if (bControl)
		play(audio_list[audio_play_index], audio_vcn);
    return flag;
}

function playchat(data)
{
    stop();
    play(data, audio_vcn);
}

function proctext(data)
{
    var flag = playcontrol_bak(data);
    if(!flag) {
        //TODO
        $.get(
            "/wx/interaction",
            {interaction: data},
            function(data) {
                if(data != "")
				{
					//首先保存打断的audio信息，用于后续持续播放
					audio_break_currentTime = window.xaudio.currentTime;
					audio_break_currentTime = audio_break_currentTime - 2;//回退两秒
					if (audio_break_currentTime < 0)
						audio_break_currentTime = 0;
					audio_break_src = window.xaudio.src;
					//alert(audio_break_src + "  111111 " + audio_break_currentTime);
					playchat(data);
				}
            }
        );
    }
}

function deal_nlu(data, result)
{
    console.log("===>>> deal nlu.");
    console.log("===>>> domain:", result['domain']);
    if(result['domain'] == "speech" || result['domain'] == "volume") {
        playcontrol(result);
    } else {
        $.get(
            "/wx/interaction",
            {interaction: data},
            function(data) {
                if(data != "") {
					//首先保存打断的audio信息，用于后续持续播放
					audio_break_currentTime = window.xaudio.currentTime;
					audio_break_currentTime = audio_break_currentTime - 2;//回退两秒
					if (audio_break_currentTime < 0)
						audio_break_currentTime = 0;
					audio_break_src = window.xaudio.src;
					//alert(audio_break_src + "  111111 " + audio_break_currentTime);
					playchat(data);
				}
            }
        );
    }
}

var nlu_url = "http://www.test.com/textCmd"
function nlu_proc(data, userid)
{
    str_id = 'test_' + userid;
    json_data = {
        "userid" : str_id,
        "words" : data
    };
    console.log(json_data);

    $.post(
        "/textCmd",
        JSON.stringify(json_data),
        function(result) {
            console.log(result)
            deal_nlu(data, eval('(' + result + ')'));
        }
    );
    /*
    $.ajax({
        url: nlu_url,
        type: "POST",
        //contentType: "application/json;charset=utf-8",
        data: json_data,
        dataType : "json",
        success : function(result) {
            console.log(result)
            deal_nlu(data, result);
        },
        error:function(msg) {
        }
    });
    */
}
