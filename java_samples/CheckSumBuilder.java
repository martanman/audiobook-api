package com.listenbook.god.model.resp;

import android.support.v4.media.j;
import cn.hutool.core.util.RandomUtil;
import java.security.MessageDigest;
import java.util.Random;
/* loaded from: classes4.dex */
public class CheckSumBuilder {
    private static final char[] HEX_DIGITS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};

    private static String encode(String str, String str2) {
        if (str2 == null) {
            return null;
        }
        try {
            MessageDigest messageDigest = MessageDigest.getInstance(str);
            messageDigest.update(str2.getBytes());
            return getFormattedText(messageDigest.digest());
        } catch (Exception e10) {
            throw new RuntimeException(e10);
        }
    }

    public static String getCheckSum(String str, String str2, String str3) {
        return encode("sha1", j.c(str, str2, str3));
    }

    private static String getFormattedText(byte[] bArr) {
        int length = bArr.length;
        StringBuilder sb2 = new StringBuilder(length * 2);
        for (int i10 = 0; i10 < length; i10++) {
            char[] cArr = HEX_DIGITS;
            sb2.append(cArr[(bArr[i10] >> 4) & 15]);
            sb2.append(cArr[bArr[i10] & 15]);
        }
        return sb2.toString();
    }

    public static String getMD5(String str) {
        return encode("md5", str);
    }

    public static String getRandomString(int i10) {
        Random random = new Random();
        StringBuilder sb2 = new StringBuilder();
        for (int i11 = 0; i11 < i10; i11++) {
            sb2.append(RandomUtil.BASE_CHAR_NUMBER.charAt(random.nextInt(36)));
        }
        return sb2.toString();
    }
}

