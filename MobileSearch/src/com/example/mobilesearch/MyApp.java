package com.example.mobilesearch;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import android.app.Application;
import android.os.Environment;
import android.util.Log;


public class MyApp extends Application {
	public String user_id;
	File path = new File(Environment.getExternalStorageDirectory().toString()+"/data");
	
	public void set_user(String s) {
		user_id = s;
		boolean find = false;
		try {
			File dir = new File(Environment.getExternalStorageDirectory().toString()+"/data/"+user_id+"_mobile_search");
			if (!dir.exists()) {
				   dir.mkdirs();
			}
		}
		catch(Exception e){   
			e.printStackTrace();
		}  
		
	}

	public String get_user() {
		return user_id;
	}
	
}
