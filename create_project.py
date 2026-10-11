from pathlib import Path

files = {
'settings.gradle.kts': '''pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "NumberChecks"
include(":app")
''',
'build.gradle.kts': '''plugins {
    id("com.android.application") version "8.7.3" apply false
}
''',
'app/build.gradle.kts': '''plugins { id("com.android.application") }

android {
    namespace = "com.example.numberchecks"
    compileSdk = 35
    defaultConfig {
        applicationId = "com.example.numberchecks"
        minSdk = 23
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
''',
'app/src/main/AndroidManifest.xml': '''<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application android:label="Числа 001–999" android:theme="@android:style/Theme.Material.Light.NoActionBar" android:allowBackup="false" android:supportsRtl="true">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
''',
'app/src/main/java/com/example/numberchecks/MainActivity.java': '''package com.example.numberchecks;

import android.app.Activity;
import android.os.Bundle;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.view.View;
import android.view.ViewGroup;
import android.widget.*;

public class MainActivity extends Activity {
    private SharedPreferences preferences;
    private final boolean[] selected = new boolean[1000];
    private TextView counter;
    private int count;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        preferences = getSharedPreferences("numbers", MODE_PRIVATE);
        for (int n = 1; n <= 999; n++) {
            selected[n] = preferences.getBoolean("n" + n, false);
            if (selected[n]) count++;
        }

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Color.rgb(247, 248, 252));
        root.setPadding(dp(12), dp(8), dp(12), 0);
        // Отступы от системных панелей, в том числе на Android 15+.
        root.setOnApplyWindowInsetsListener((v, insets) -> {
            v.setPadding(dp(12) + insets.getSystemWindowInsetLeft(),
                dp(8) + insets.getSystemWindowInsetTop(),
                dp(12) + insets.getSystemWindowInsetRight(),
                insets.getSystemWindowInsetBottom());
            return insets.consumeSystemWindowInsets();
        });

        TextView title = new TextView(this);
        title.setText("Числа 001–999");
        title.setTextSize(26);
        title.setTextColor(Color.rgb(25, 32, 55));
        root.addView(title);

        counter = new TextView(this);
        counter.setTextSize(16);
        counter.setPadding(0, dp(8), 0, dp(16));
        root.addView(counter);
        updateCounter();

        GridView grid = new GridView(this);
        grid.setId(1001);
        grid.setNumColumns(2);
        grid.setHorizontalSpacing(dp(8));
        grid.setVerticalSpacing(dp(8));
        grid.setStretchMode(GridView.STRETCH_COLUMN_WIDTH);
        grid.setClipToPadding(false);
        grid.setPadding(0, 0, 0, dp(12));
        grid.setAdapter(new NumberAdapter());
        root.addView(grid, new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f));
        setContentView(root);
        root.requestApplyInsets();
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    private void updateCounter() {
        counter.setText("Выбрано: " + count + " из 999");
    }

    private void paint(CheckBox box, boolean checked) {
        android.graphics.drawable.GradientDrawable background =
            new android.graphics.drawable.GradientDrawable();
        background.setCornerRadius(dp(12));
        background.setColor(checked ? Color.rgb(210, 230, 255) : Color.WHITE);
        box.setBackground(background);
    }

    private class NumberAdapter extends BaseAdapter {
        @Override public int getCount() { return 999; }
        @Override public Object getItem(int position) { return position + 1; }
        @Override public long getItemId(int position) { return position + 1; }
        @Override public boolean hasStableIds() { return true; }

        @Override public View getView(int position, View recycled, ViewGroup parent) {
            final int number = position + 1;
            CheckBox box;
            if (recycled instanceof CheckBox) {
                box = (CheckBox) recycled;
            } else {
                box = new CheckBox(MainActivity.this);
                box.setTextSize(22);
                box.setTextColor(Color.rgb(25, 32, 55));
                box.setPadding(dp(12), dp(8), dp(12), dp(8));
                box.setMinHeight(dp(72));
                box.setLayoutParams(new AbsListView.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
            }
            box.setOnCheckedChangeListener(null);
            box.setText(String.format(java.util.Locale.ROOT, "%03d", number));
            box.setChecked(selected[number]);
            paint(box, selected[number]);
            box.setOnCheckedChangeListener((button, checked) -> {
                if (selected[number] != checked) {
                    selected[number] = checked;
                    count += checked ? 1 : -1;
                    preferences.edit().putBoolean("n" + number, checked).apply();
                    updateCounter();
                }
                paint((CheckBox) button, checked);
            });
            return box;
        }
    }
}
''',
}

for name, content in files.items():
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
print('Android project created.')
