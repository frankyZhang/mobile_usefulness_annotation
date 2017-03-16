package com.example.mobilesearch;

import android.content.Context;
import android.util.AttributeSet;
import android.util.Log;
import android.webkit.WebView;


public class MyWebView extends WebView {
	public OnScrollChangeListener listener;
	
	public MyWebView(Context context, AttributeSet attrs, int defStyle) {
		super(context, attrs, defStyle);
	}

	public MyWebView(Context context, AttributeSet attrs) {
		super(context, attrs);
	}

	public MyWebView(Context context) {
		super(context);
	}

	@Override
	protected void onScrollChanged(int l, int t, int oldl, int oldt) {
		super.onScrollChanged(l, t, oldl, oldt);
		listener.onScrollChanged(l, t, oldl, oldt);
	}

	public void setOnScrollChangeListener(OnScrollChangeListener listener) {

		this.listener = listener;

	}

	public interface OnScrollChangeListener {
		public void onScrollChanged(int l, int t, int oldl, int oldt);

	}	
	
}
