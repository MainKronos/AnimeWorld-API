window.onload = function() {
  //<editor-fold desc="Changeable Configuration Block">

  // the following lines will be replaced by docker/configurator, when it runs in a docker-container
  window.ui = SwaggerUIBundle({
    url: "swagger.yaml",
    dom_id: '#swagger-ui',
    deepLinking: true,
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    plugins: [
      SwaggerUIBundle.plugins.DownloadUrl
    ],
    layout: "StandaloneLayout",


    tryItOutEnabled: true,
    withCredentials: true,
    persistAuthorization: true,
    requestInterceptor: (req) => {
        if(!('loadSpec' in req)){
            console.log(req);
            document.cookie = req.headers['Cookie'];

        }
        return req;
    }
  });

  //</editor-fold>
};
