package com.example.mobilesearch;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;


public class MainActivity extends Activity {
	
	private MyApp myapp;
	private EditText user_id;
	private Button begin_button;
	private ButtonClickedListener buttonClickedListener;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		this.myapp = (MyApp) this.getApplication();
		this.user_id = (EditText) this.findViewById(R.id.user_id);
		this.begin_button = (Button) this.findViewById(R.id.begin_button);
		this.buttonClickedListener = new ButtonClickedListener();
		
		this.begin_button.setOnClickListener(buttonClickedListener);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}
	
	private class ButtonClickedListener implements OnClickListener{
		public void onClick(View v) {
			Log.v("log in main_activity", ""+System.currentTimeMillis());
			String s = user_id.getText().toString().trim();
			if(s.length() != 10){
				AlertDialog alertdialog = new AlertDialog.Builder(MainActivity.this)
						//.setIcon(android.R.drawable.btn_star_big_on)
						.setTitle("学号不对!")
						.setMessage("请输入10位数字的学号")
						.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
							@Override
							public void onClick(DialogInterface dialog, int which) {
								// TODO Auto-generated method stub
							}
						})
						.show();
			}
			else {
				myapp.set_user(s);
				Log.v("log in main_activity", "done");
				Intent intent = new Intent(MainActivity.this, WebBrowser.class);
				startActivity(intent);
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
