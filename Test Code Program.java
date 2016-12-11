 public boolean isConnectInternet(Context context) {
        ConnectivityManager connectivityManager = (ConnectivityManager) 
         context.getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connectivityManager.getActiveNetworkInfo();
        return (networkInfo != null && networkInfo.isConnected()) ? true : false;
    }
