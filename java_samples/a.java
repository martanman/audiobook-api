package ia;

import androidx.core.os.EnvironmentCompat;
import cd.t;
import com.google.gson.Gson;
import com.listenbook.god.constant.AppConst;
import com.listenbook.god.model.resp.CheckSumBuilder;
import com.listenbook.god.model.resp.CheckSumDTO;
import df.i;
import java.net.URLEncoder;
import java.util.Date;
import okhttp3.Interceptor;
import okhttp3.Request;
import okhttp3.Response;
/* compiled from: Interceptor.kt */
/* loaded from: classes4.dex */
public final class a implements Interceptor {
    @Override // okhttp3.Interceptor
    public final Response intercept(Interceptor.Chain chain) {
        i.f(chain, "chain");
        Request request = chain.request();
        String valueOf = String.valueOf(System.currentTimeMillis());
        String randomString = CheckSumBuilder.getRandomString(8);
        String checkSum = CheckSumBuilder.getCheckSum("tingshu3dbeb952d32d8a7f30f5dd88", randomString, valueOf);
        T value = t.f1964b.getValue();
        i.e(value, "<get-MYGSON>(...)");
        i.e(randomString, "nonce");
        i.e(checkSum, "checkSum");
        String packageName = gk.a.b().getPackageName();
        i.e(packageName, "appCtx.packageName");
        String json = ((Gson) value).toJson(new CheckSumDTO("20210621161", randomString, valueOf, checkSum, packageName, AppConst.a().getVersionName()));
        Request.Builder newBuilder = request.newBuilder();
        newBuilder.header("model", "Android");
        i.e(json, "checkSha");
        newBuilder.header("checkSumDTO", json);
        String packageName2 = gk.a.b().getPackageName();
        i.e(packageName2, "appCtx.packageName");
        newBuilder.header("packageId", packageName2);
        newBuilder.header("version", AppConst.a().getVersionName());
        String encode = URLEncoder.encode(String.valueOf(new Date()), "utf-8");
        i.e(encode, "encode(\"${Date()}\", \"utf-8\")");
        newBuilder.header("If-Modified-Since", encode);
        String property = System.getProperty("http.agent");
        if (property == null) {
            property = EnvironmentCompat.MEDIA_UNKNOWN;
        }
        newBuilder.header("User-Agent", property);
        return chain.proceed(newBuilder.build());
    }
}

