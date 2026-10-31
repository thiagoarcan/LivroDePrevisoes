import com.android.apksig.ApkSigner;
import com.android.apksig.ApkVerifier;
import java.io.File;
import java.io.FileInputStream;
import java.security.KeyStore;
import java.security.PrivateKey;
import java.security.MessageDigest;
import java.security.cert.X509Certificate;
import java.util.Collections;

/** Small CLI around the official Apache-licensed AOSP apksig library. */
public final class ApkSignTool {
  public static void main(String[] args) throws Exception {
    if (args.length == 2 && args[0].equals("verify")) {
      verify(new File(args[1]));
      return;
    }
    if (args.length != 4 || !args[0].equals("sign")) {
      throw new IllegalArgumentException("sign INPUT OUTPUT DEBUG_KEYSTORE | verify APK");
    }
    KeyStore keys=KeyStore.getInstance("PKCS12");
    try(FileInputStream in=new FileInputStream(args[3])) { keys.load(in,"android".toCharArray()); }
    PrivateKey key=(PrivateKey)keys.getKey("androiddebugkey","android".toCharArray());
    X509Certificate cert=(X509Certificate)keys.getCertificate("androiddebugkey");
    ApkSigner.SignerConfig config=new ApkSigner.SignerConfig.Builder(
      "LOCAL_TEST",key,Collections.singletonList(cert)).build();
    new ApkSigner.Builder(Collections.singletonList(config))
      .setInputApk(new File(args[1])).setOutputApk(new File(args[2]))
      .setMinSdkVersion(26).setV1SigningEnabled(false).setV2SigningEnabled(true)
      .setV3SigningEnabled(true).setV4SigningEnabled(false).build().sign();
    verify(new File(args[2]));
  }
  private static void verify(File file) throws Exception {
    ApkVerifier.Result result=new ApkVerifier.Builder(file)
      .setMinCheckedPlatformVersion(26).setMaxCheckedPlatformVersion(36).build().verify();
    if (!result.isVerified()) throw new IllegalStateException("APK signature invalid: "+result.getErrors());
    if (!result.isVerifiedUsingV2Scheme() || !result.isVerifiedUsingV3Scheme())
      throw new IllegalStateException("Expected both APK signature schemes v2 and v3");
    System.out.println("Verified APK signatures v2 and v3 for Android API 26–36: "+file);
    for(X509Certificate c:result.getSignerCertificates()) {
      byte[] hash=MessageDigest.getInstance("SHA-256").digest(c.getEncoded());
      StringBuilder hex=new StringBuilder(); for(byte b:hash)hex.append(String.format("%02x",b&255));
      System.out.println("Signing certificate SHA-256: "+hex);
    }
    if (!result.getWarnings().isEmpty()) System.out.println("Verification warnings: "+result.getWarnings());
  }
}
