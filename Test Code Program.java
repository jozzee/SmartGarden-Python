 public boolean isConnectInternet(Context context) {
        ConnectivityManager connectMng = 
         (ConnectivityManager)context
          .getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo n = connectMng.getActiveNetworkInfo();
        return (n != null && n.isConnected()) ? true : false;
    }
