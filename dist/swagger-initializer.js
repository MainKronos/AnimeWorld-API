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
            const servers_list = document.querySelector('.servers select');
            const selected_server = servers_list.options[servers_list.selectedIndex];
            const api_root = selected_server.value;

            if(api_root == 'http://localhost:8000'){
                req.headers['X-Cookie'] = document.cookie;
            }
            console.log(req);
        }
        return req;
    }
  });

  //</editor-fold>
};
