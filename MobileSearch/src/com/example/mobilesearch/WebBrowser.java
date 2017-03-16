package com.example.mobilesearch;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.example.mobilesearch.MyWebView.OnScrollChangeListener;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.AlertDialog.Builder;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Picture;
import android.os.Bundle;
import android.os.Environment;
import android.util.AttributeSet;
import android.util.Log;
import android.view.GestureDetector;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.View.OnTouchListener;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebSettings.LayoutAlgorithm;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;

public class WebBrowser extends Activity {
	File path;
	File logfile;
	BufferedWriter logwriter;
	boolean loading=true;
	boolean search_state=false;
	boolean annotation_state=false;
	boolean jump_out_state=false;
	String old_task_id = "";
	int lognum=0;
	String logs="";
	int prey=0;
	long init_time;


	private MyApp myapp;
	
	//进度条
	private ProgressBar webProgressBar;
	
	private Button pre_button;
	private Button next_button;
	private Button finish_button;
	
	private MyWebView webView;
	private WebSettings settings;
	private WebViewClient viewClient;
	private WebChromeClient chromeClient;

	//手势
	private GestureDetector mGestureDetector;
	private GestureListener gestureListener;

	private ButtonClickedListener buttonClickedListener;
	private WebViewTouchListener webViewTouchListener;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		Log.v("log in browser", "webcreate");
		super.onCreate(savedInstanceState);
		setContentView(R.layout.webbrowser);
        this.myapp = (MyApp) this.getApplication();
        
        this.webProgressBar = (ProgressBar) this.findViewById(R.id.web_progress_bar);
        
        this.webView = (MyWebView) this.findViewById(R.id.webview);
		this.settings = this.webView.getSettings();
		this.viewClient = new OwnerWebView();
		this.chromeClient = new OwnerChromeClient();
		
		this.pre_button = (Button) this.findViewById(R.id.pre_button);
		this.next_button = (Button) this.findViewById(R.id.next_button);
		this.finish_button = (Button) this.findViewById(R.id.finish_button);

		this.buttonClickedListener = new ButtonClickedListener();
		this.webViewTouchListener = new WebViewTouchListener();
		
		this.gestureListener = new GestureListener();
		this.mGestureDetector = new GestureDetector(this, gestureListener);

		this.settings.setDefaultTextEncodingName("UTF-8");
		this.settings.setJavaScriptEnabled(true);
		this.settings.setSupportZoom(true); 
		//this.settings.setCacheMode(WebSettings.LOAD_CACHE_ELSE_NETWORK);  //关闭webview中缓存 
		//this.settings.setAppCacheEnabled(true);  
		webView.setDrawingCacheEnabled(true);
		

		this.webView.setWebViewClient(this.viewClient);
		this.webView.setWebChromeClient(this.chromeClient);
		this.pre_button.setEnabled(true);
		this.next_button.setEnabled(true);
		
		this.pre_button.setOnClickListener(buttonClickedListener);
		this.next_button.setOnClickListener(buttonClickedListener);
		this.finish_button.setOnClickListener(buttonClickedListener);
		this.webView.setOnTouchListener(this.webViewTouchListener);
		this.webView.setOnScrollChangeListener(new OnScrollChangeListener() {
			@Override
			public void onScrollChanged(int l, int t, int oldl, int oldt) {
				//滑动中
				//Log.v("mylog","Y = " + webView.getScrollY());
				String current_url = webView.getUrl();
				if (is_serp(current_url)) {
					String task_id = get_task_id(current_url);
						/*if (!returnp) {
							webView.scrollTo(0, prey);
							returnp=true;
						}
						else {
							Log.v("mylog","current Y = " + t+'\t'+webView.getContentHeight()+'\t'+webView.getScale());
							writeinlog("YCHANGE","Y="+t);
						}*/
					Log.v("log in ychange, task"+task_id, "current Y = " + t + '\t' + webView.getContentHeight() + '\t' + webView.getScale());
					writenlog(task_id, "YCHANGE", "Y="+t);
				}
				else {
					if (search_state){
						writenlog(old_task_id, "YCHANGE_IN_LP", "Y="+t);
					}
				}
			}
			
		});
		Log.v("log in browser", "webbrowserfinish");
		init();
	}
	
	private void init() {
		String filename = myapp.get_user()+".log";
		path = new File(Environment.getExternalStorageDirectory().toString()+"/data/"+myapp.get_user()+"_mobile_annotation");;
		logfile = new File(path, filename);
		
		try {
			logwriter = new BufferedWriter(new FileWriter(logfile,true));
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		this.webView.loadUrl("http://10.129.248.85:8000/login");
		init_time=System.currentTimeMillis();
		//pre_button.setVisibility(View.GONE);
		//next_button.setVisibility(View.GONE);
		finish_button.setVisibility(View.GONE);
	}
	

	@SuppressWarnings("deprecation")
	public void writenlog(String task_id, String action, String info) {
		if (task_id.equals("0"))
			return;
		long timestamp=System.currentTimeMillis();
		try {
			Log.v("log in writer, task"+task_id, action+' '+info);
			lognum+=1;

			if (!task_id.equals(old_task_id)) {
				logs+="TIME="+timestamp+"\tTask="+task_id+"\tACTION=TASK_BEGIN\tINFO:\t";
				logs+="viewheight="+webView.getHeight()+"\tcontentheight="+webView.getContentHeight()+"\tscale="+webView.getScale()+"\n";
				old_task_id = task_id;
				//get_pic();
			}
			logs+="TIME="+timestamp+"\tTask="+task_id+"\tACTION="+action+"\tINFO:\t"+info+'\n';

			if (lognum==100 || action.equals("FINISH") || action.equals("TASK_FINISH")) {
				logwriter.write(logs);
				logwriter.flush();
				logs="";
				lognum=0;
			}
			if (action.equals("FINISH")) {
				logwriter.close();
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	
	private class OwnerWebView extends WebViewClient{
		@Override
		public boolean shouldOverrideUrlLoading(WebView view, String url) {
			//view.loadUrl(url);
			//Log.v("mylog", current_url);
			return false;
		}

		@Override
		public void onReceivedError(WebView view, int errorCode,
				String description, String failingUrl) {
			super.onReceivedError(view, errorCode, description, failingUrl);
			if(errorCode==WebViewClient.ERROR_HOST_LOOKUP){
				//找不到页面，调用百度搜搜
				//url = "http://www.baidu.com/baidu?word=" + url;
				//webView.loadUrl(url);
			}else if(errorCode==WebViewClient.ERROR_UNSUPPORTED_SCHEME){
				//不支持协议
				
				//if(failingUrl.trim().equals("javascript:;")){
					//不支持javascript					
				//}
			}
		}

		@Override
		public void onPageStarted(WebView view, String url, Bitmap favicon) {
			super.onPageStarted(view, url, favicon);
			if (is_review(url)) {
				search_state = false;
				writenlog(old_task_id, "TASK_FINISH", "");
			}
			if(is_tasks(url)){
				annotation_state = false;
			}
			if (is_annotation(url)) {
				annotation_state = true;
			}
			if (annotation_state) {
				if (is_annotation(url)){
					if(jump_out_state){
						jump_out_state=false;
					}
				}
				else {
					if (!jump_out_state){
						jump_out_state=true;
					}
				}
			}
			if (is_finished(url)){
				finish_button.setVisibility(View.VISIBLE);
			}
			if (is_serp(url)) {
				search_state = true;
			}
			if (search_state) {
				if (is_serp(url)) {
						if (jump_out_state) {
							jump_out_state = false;
							writenlog(old_task_id, "BACK_TO_SERP", "");
						}
				}
				else {
						if (!jump_out_state) {
							jump_out_state = true;
							writenlog(old_task_id, "CLICK_RESULT", "URL=" + url);
						}
						writenlog(old_task_id, "JUMP_TO_PAGE", "URL=" + url);
				}
			}
			if (jump_out_state){
				pre_button.setVisibility(View.VISIBLE);
				next_button.setVisibility(View.VISIBLE);
			}
			else {
				//pre_button.setVisibility(View.GONE);
				//next_button.setVisibility(View.GONE);
			}
		}

		@Override
		public void onPageFinished(WebView view, String url){
			super.onPageFinished(view, url);
			/*if (search_state){
				if (!is_serp(url)){
					if (!jump_out_state) {
						jump_out_state = true;
						writenlog(old_task_id, "CLICK_RESULT", "TITLE=" + webView.getTitle() + "\tURL=" + webView.getUrl());
					}
					writenlog(old_task_id, "JUMP_TO_PAGE", "TITLE=" + webView.getTitle() + "\tURL=" + webView.getUrl());
				}
			}*/
		}

	}
	
	/*
	private String get_query(String url) {
		
		Pattern pattern=Pattern.compile("(?<=q=)(.*?)(?=&)");
		Matcher matcher = pattern.matcher(url+"&");
		String s="";
		if (matcher.find()) {
			s=matcher.group(0);
			try {
				s=URLDecoder.decode(s, "UTF-8");
			} catch (UnsupportedEncodingException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			Log.v("mylog", "!!!"+s);
		}
		return s;
	}*/

	private String get_task_id(String url) {
		Pattern pattern = Pattern.compile("(.*)/search/(\\d{10})/(\\d{1,2})/(.*?)/");
		Matcher matcher = pattern.matcher(url);
		String s = "";
		if (matcher.find()) {
			s = matcher.group(4);
			//Log.v("log in get task", "id" + s);
		}
		//else
			//Log.v("Log in get task", "fail");
		return s;
	}

	private boolean is_serp(String url) {
		String sub="http://10.129.248.85:8000/search/";
		int pos = url.indexOf(sub);
		if (pos!=-1)
			return true;
		else
			return false;
	}

	private boolean is_review(String url) {
		String sub="http://10.129.248.85:8000/taskreview/";
		int pos = url.indexOf(sub);
		if (pos!=-1)
			return true;
		else
			return false;
	}

	private boolean is_annotation(String url) {
		String sub="http://10.129.248.85:8000/annotation/";
		int pos = url.indexOf(sub);
		if (pos!=-1)
			return true;
		else
			return false;
	}

	private boolean is_tasks(String url) {
		String sub="http://10.129.248.85:8000/tasks/";
		int pos = url.indexOf(sub);
		if (pos!=-1)
			return true;
		else
			return false;
	}

	private boolean is_finished(String url) {
		String sub="http://10.129.248.85:8000/tasks/finished/";
		int pos = url.indexOf(sub);
		if (pos!=-1)
			return true;
		else
			return false;
	}
	/**
	 * WebChromeClient自定义继承类
	 * 覆盖如下方法
	 * 1.	onProgressChanged
	 * 		用来解决进度条显示问题
	 * */
	private class OwnerChromeClient extends WebChromeClient{
		@Override
		public void onProgressChanged(WebView view, int newProgress) {
			super.onProgressChanged(view, newProgress);
			//MainActivity.this.setProgress(newProgress * 100);
			if(newProgress==100){
				webProgressBar.setVisibility(View.GONE);
				//webView.setVisibility(View.VISIBLE);
				Log.v("log in browser", "100%");
			}
			else{
				changeStatueOfWebToolsButton();
				//Log.v("log in browser", "change");
				if (loading) {
					//webView.setVisibility(View.GONE);
					webProgressBar.setVisibility(View.VISIBLE);
					webProgressBar.setProgress(newProgress);
				}
			}
		}
		
	}
	
	/**
	 * OnTouchListener自定义继承类
	 * 解决将手势交给GestureDetector类解决
	 * */
	private class WebViewTouchListener implements OnTouchListener{

		@Override
		public boolean onTouch(View v, MotionEvent event) {
			if(v.getId()==R.id.webview){
				//Log.i(DEG_TAG, "info :webViewTouched");
				//Log.i(DEG_TAG, "event:"+event.describeContents());
				return mGestureDetector.onTouchEvent(event);
			}
			return false;
		}
		
	}
	
	/**
	 * GestureDetector.OnGestureListener自定义继承类
	 * 解决各种手势的相对应策略
	 * 1.	向上滑动webView到顶触发事件，显示地址栏
	 * 2.	向下滑动webView触发时间，隐藏地址栏
	 * */
	private class GestureListener implements GestureDetector.OnGestureListener{

		@Override
		public boolean onDown(MotionEvent e) {
			//Log.v("mylog", "onDown");
			return false;
		}

		@Override
		public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX,
				float velocityY) {
			String current_url = webView.getUrl();
			if (is_serp(current_url)){
				String task_id = get_task_id(current_url);
				Log.v("log in fling, task"+task_id, "onFling webView Y:"+webView.getScrollY());
				Log.v("log in fling, task"+task_id,"onFling "+e1.getX()+'\t'+e1.getY()+'\t'+e2.getX()+'\t'+e2.getY());
				Log.v("log in fling, task"+task_id, "vx="+velocityX+"\tvy="+velocityY);
				writenlog(task_id, "FLING","X1="+e1.getX()+"\tY1="+e1.getY()+"\tX2="+e2.getX()+"\tY2="+e2.getY()+"\tVX="+velocityX+"\tVY="+velocityY);
			}
			else {
				if(search_state){
					Log.v("fling in lp", "...");
					writenlog(old_task_id, "FLING_IN_LP","X1="+e1.getX()+"\tY1="+e1.getY()+"\tX2="+e2.getX()+"\tY2="+e2.getY()+"\tVX="+velocityX+"\tVY="+velocityY);

				}
			}
				return false;
		}

		@Override
		public void onLongPress(MotionEvent e) {
			String current_url = webView.getUrl();
			if (is_serp(current_url)) {
				String task_id = get_task_id(current_url);
					Log.v("log in longpress, task"+task_id, "onLongPress");
					writenlog(task_id, "LONGPRESS", "X=" + e.getX() + "\tY=" + e.getY() + "\tT=" + (e.getEventTime() - e.getDownTime()));
				}

			else {
				if(search_state){
					writenlog(old_task_id, "LONGPRESS_IN_LP","X=" + e.getX() + "\tY=" + e.getY() + "\tT=" + (e.getEventTime() - e.getDownTime()));

				}
			}
		}

		@Override
		public boolean onScroll(MotionEvent e1, MotionEvent e2,
				float distanceX, float distanceY) {
			String current_url = webView.getUrl();
			if (is_serp(current_url)) {
				String task_id = get_task_id(current_url);
					Log.v("log in scroll, task"+task_id, "onScroll webView Y:" + webView.getScrollY());
					Log.v("log in scroll, task"+task_id, "onScroll " + e1.getX() + '\t' + e1.getY() + '\t' + e2.getX() + '\t' + e2.getY());
					writenlog(task_id,"SCROLL", "X1=" + e1.getX() + "\tY1=" + e1.getY() + "\tX2=" + e2.getX() + "\tY2=" + e2.getY());
			}
			else {
				if(search_state){
					Log.v("scroll in lp", "...");
					writenlog(old_task_id, "SCROLL_IN_LP","X1=" + e1.getX() + "\tY1=" + e1.getY() + "\tX2=" + e2.getX() + "\tY2=" + e2.getY());

				}
			}
			return false;
		}

		@Override
		public void onShowPress(MotionEvent e) {
			//Log.v("mylog", "onShowPress");
		}

		@Override
		public boolean onSingleTapUp(MotionEvent e) {
			String current_url = webView.getUrl();
			if (is_serp(current_url)) {
				String task_id = get_task_id(current_url);
					Log.v("log in tapup, task" + task_id, "onSingleTapUp");
					prey = webView.getScrollY();
					writenlog(task_id, "SINGLETAPUP", "X=" + e.getX() + "\tY=" + e.getY());
			}
			else {
				if(search_state){
					Log.v("tap up in lp", "...");
					writenlog(old_task_id, "SINGLETAPUP_IN_LP","X=" + e.getX() + "\tY=" + e.getY());
				}
			}
			return false;
		}
		
	}

	/**
	 * 设置工具栏回溯历史是否可用
	 * */
	private void changeStatueOfWebToolsButton(){
		if(webView.canGoBack()){
			//设置可使用状态
			pre_button.setEnabled(true);
		}else{
			//设置禁止状态
			pre_button.setEnabled(false);
		}
		if(webView.canGoForward()){
			//设置可使用状态
			next_button.setEnabled(true);
		}else{
			//设置禁止状态
			next_button.setEnabled(false);
		}
	}

	private class ButtonClickedListener implements OnClickListener{
		public void onClick(View v) {
			switch (v.getId()) {
			case R.id.finish_button:
				AlertDialog alertdialog = new AlertDialog.Builder(WebBrowser.this)
						//.setIcon(android.R.drawable.btn_star_big_on)
						.setTitle("是否完成？")
						.setPositiveButton("Yes", new DialogInterface.OnClickListener() {

							@Override
							public void onClick(DialogInterface dialog, int which) {
								// TODO Auto-generated method stub
								Log.v("log in browser", "All_finish");
								writenlog(old_task_id, "FINISH", "all tasks finished");
								Intent intent = new Intent(WebBrowser.this,Thanks.class);
								startActivity(intent);
							}
						})
						.setNegativeButton("No",  new DialogInterface.OnClickListener() {

							@Override
							public void onClick(DialogInterface dialog, int which) {
								// TODO Auto-generated method stub
							}
						})
						.show();
				break;
			case R.id.pre_button:
				if(webView.canGoBack()){
					//后退
					webView.goBack();
				}
				break;
			case R.id.next_button:
				if(webView.canGoForward()){
					//前进
					webView.goForward();
				}
				break;
			default:
				break;
			}
		}
	}
	
	@Override
	public boolean onKeyDown(int keyCode, KeyEvent event) {
	    if(keyCode == KeyEvent.KEYCODE_BACK) { //监控/拦截/屏蔽返回键
	        return true;
	    } else if(keyCode == KeyEvent.KEYCODE_MENU) {//MENU键
	        //监控/拦截菜单键
	         return true;
	    }     
	return super.onKeyDown(keyCode, event);
	}
}
