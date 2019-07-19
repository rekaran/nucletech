var app = new Vue({
    el: '#nt-app',
    delimiters: ['<%', '%>'],
    beforeCreate(){
      let self = this;
      let csrf_key = document.getElementById("csrf_token");
      let project_key = document.getElementById("project_key");
      let project_hash = document.getElementById("project_hash");
      let user_key = document.getElementById("user_key");
      let data = {
        key: project_key.value,
        hash: project_hash.value,
      }
      const url = "http://127.0.0.1:8000/datamanager/"+project_hash.value+"/";
      const Http = new XMLHttpRequest();
      Http.open("POST", url, true);
      Http.setRequestHeader("token", user_key.value);
      Http.setRequestHeader("X-CSRFToken", csrf_key.value);
      Http.send(JSON.stringify(data));
      Http.onload = () =>{
        if (Http.status == 200) {
          let data = JSON.parse(Http.responseText);
          self.flow = data.flow;
          self.faq = data.faq;
          self.smalltalks = data.smalltalk;
          self.datamatrix = data.datamatrix;
        }
      }
    },
    data: {
      flow: [],// Side nav flow display
      faq: [],// Side nav faq display,
      smalltalks: [],// Small talks display in FAQ Sections
      datamatrix: {},// Keeps track of data
      current_faq: [],//Toggle between faq and smalltalks
      current_faq_type: "",
      current_flow_name: "",
      current_stages: [],
      flow_variations: [],
      faq_variations: [],
      flow_index: '',
      flow_index_type: '',
      is_home: true,
      is_flow: false,
      is_faq: false,
      is_validation: false,
      is_bot_greetings: false,
      is_settings: false,
      user_input_type: 'Text',
      user_add_button: false,
      user_input_buttons: [],
      user_add_carousel: false,
      user_input_carousels: [],
      user_validation_type: "No Validation",
      user_validation: "",
      user_valid_next: "",
      invalid_message: "",
      user_validation_type_: "no",
      bot_says_error: "",
      bot_buttons_error: "",
      bot_carousels_error: "",
      bot_validation_error: "",
      variation_validation_error: "",
      faq_variation_validation_error: "",
      faq_answer_validation_error: "",
      faq_name_validation_error: "",
    },
    methods: {
      enable_flow(type){
        let self = this;
        self.is_faq = false;
        self.is_home = false;
        self.is_flow = true;
        self.is_settings = false;
        self.clear_flow();
        if(type=="new"){
          self.current_flow_name="flow"+self.flow.length;
          self.flow_index = self.flow.length;
          self.flow_index_type = "new";
        }else{
          self.flow_index = type
          self.flow_index_type = "exist";
          self.current_stages = self.flow[type].stages;
          self.current_flow_name = self.flow[type].name;
          self.flow_variations = self.flow[type].variation;
        }
      },
      enable_faq(type){
        let self = this;
        self.is_faq = true;
        self.is_home = false;
        self.is_flow = false;
        self.is_settings = false;
        if(type=="smalltalks"){
          self.current_faq = self.smalltalks;
          self.current_faq_type = "SMALLTALK";
        }else if(type=="custom"){
          self.current_faq = self.faq;
          self.current_faq_type = "CUSTOM";
        }
      },
      enable_setting(){
        let self = this;
        self.is_faq = false;
        self.is_home = false;
        self.is_flow = false;
        self.is_settings = true;
      },
      home_view(type){
        let self = this;
        self.is_faq = false;
        self.is_home = true;
        self.is_flow = false;
        self.is_settings = false;
      },
      add_faq_variation(){
        let self = this;
        let variation = document.getElementById("faq-variation");
        if(variation.value==""){
          self.faq_variation_validation_error = "Variation cannot be empty";
        }else{
          if(self.faq_variations.indexOf(variation.value)==-1){
            self.variation_validation_error = "";
            self.faq_variations.push(variation.value);
          }else{
            self.faq_variation_validation_error = "Variation already exists";
          }
          variation.value = "";
        }
      },
      delete_faq_variation(idx){
        let self = this;
        self.faq_variations.splice(idx, 1);
      },
      add_faq(){
        let self = this;
        let faq_name = document.getElementById("faq-name");
        let faq_answer = document.getElementById("faq-answer");
        if (faq_name.value==""){
          self.faq_name_validation_error = "Name cannot be empty";
        }else{
          self.faq_name_validation_error = "";
          if(faq_answer.value==""){
            self.faq_answer_validation_error = "Answer cannot be empty";
          }else{
            self.faq_answer_validation_error = "";
            if(self.faq_variations.length==0){
              self.faq_variation_validation_error = "Atleast one variation must be present";
            }else{
              self.faq_variation_validation_error = "";
              self.faq.forEach(faq=>{
                if(faq.name===faq_name.value){
                  self.faq_name_validation_error = 'FAQ with name "'+faq_name.value+'" already exists';
                }
              });
              if(self.faq_name_validation_error==""){
                let data = {
                  name: faq_name.value,
                  answer: faq_answer.value,
                  variation: self.faq_variations,
                  active: true
                }
                self.faq.push(data);
                self.current_faq = self.faq;
                faq_name.value = "";
                faq_answer.value = "";
                self.faq_variations = [];
                UIkit.modal("#nt-faqmodal").hide();
              }
            }
          }
        }
      },
      add_flow_variation(){
        let self = this;
        let variation = document.getElementById("add-variation")
        if(variation.value==""){
          self.variation_validation_error = "Variation cannot be empty"
        }else{
          if(self.flow_variations.indexOf(variation.value)==-1){
            self.variation_validation_error = ""
            self.flow_variations.push(variation.value)
          }else{
            self.variation_validation_error = "Variation already exists"
          }
          variation.value = ""
        }
      },
      add_user_button(){
        let self = this;
        let button_value = document.getElementById("nt-user-button-bot-text");
        let button_text = document.getElementById("nt-user-button-text");
        let button_jump = document.getElementById("nt-user-button-bot-jump");
        let jump = button_jump.value;
        if(jump==""){
          jump = "next";
        }else{
          self.current_stages.forEach((stg, idx)=>{
            if(stg.stage_name==jump){
              jump = idx;
            }
          });
        }
        self.user_input_buttons.push({value: button_value.value, text: button_text.value, jump: jump});
        button_text.value = "";
        button_value.value = "";
        button_jump.value = "";
        self.user_add_button = false;
      },
      add_user_carousel(){
        let self = this;
        let carousel_text = document.getElementById("nt-user-carousel-text");
        let carousel_value = document.getElementById("nt-user-carousel-bot-text");
        let carrousel_jump = document.getElementById("nt-user-carousel-bot-jump");
        let jump = carrousel_jump.value;
        if(jump==""){
          jump = "next";
        }else{
          self.current_stages.forEach((stg, idx)=>{
            if(stg.stage_name==jump){
              jump = idx;
            }
          });
        }
        self.user_input_carousels.push({value: carousel_value.value, text: carousel_text.value, jump: jump});
        carousel_text.value = "";
        carousel_value.value = "";
        carrousel_jump.value = "";
        self.user_add_carousel = false;
      },
      add_user_validation(){
        let self = this;
        let input_validation = "";
        let input_validation_type = "";
        let input_valid_next = "";
        let invalid_message = "";
        if(self.user_validation_type=="No Validation"){
          input_validation_type='no';
        }else if(self.user_validation_type=="API Validation"){
          input_validation_type="api";
          let valid_source = document.getElementById("nt-api-validation");
          let invalid_msg = document.getElementById("nt-invalid-message");
          input_validation = valid_source.value;
          invalid_message = invalid_msg.value;
          valid_source.value = "";
          invalid_msg.value = "I'm not able to understand you input.";
        }else if(self.user_validation_type=="Regex Validation"){
          input_validation_type="regex";
          let valid_source = document.getElementById("nt-regex-validation");
          let invalid_msg = document.getElementById("nt-invalid-message");
          input_validation = valid_source.value;
          invalid_message = invalid_msg.value;
          valid_source.value = "";
          invalid_msg.value = "I'm not able to understand you input.";
        }
        if(input_validation_type!="no"){
          if(input_validation==""){
            self.bot_validation_error="This field cannot be blank!";
            return;
          }
        }
        let input_validated = document.getElementById("nt-validated");
        if(input_validated.value=="Continue Flow"){
          input_valid_next="next";
        }else if(input_validated.value=="Exit Flow"){
          input_valid_next="exit";
        }
        input_validated.value = "Continue Flow";
        self.user_validation = input_validation;
        self.user_valid_next = input_valid_next;
        self.invalid_message = invalid_message;
        self.user_validation_type_ = input_validation_type;
        self.is_validation = false;
      },
      delete_button(idx){
        let self = this;
        self.user_input_buttons.splice(idx, 1);
      },
      delete_carousel(idx){
        let self = this;
        self.user_input_carousels.splice(idx, 1);
      },
      delete_vatiation(idx){
        let self = this;
        self.flow_variations.splice(idx, 1);
      },
      clear_stage(){
        let self = this;
        self.user_input_type = 'Text';
        self.user_validation_type = "No Validation";
        self.user_validation_type="No Validation";
        self.user_validation = "";
        self.user_valid_next = "";
        self.invalid_message = "";
        self.user_validation_type_ = "no";
        self.bot_says_error= "";
        self.bot_buttons_error= "";
        self.bot_carousels_error= "";
        self.bot_validation_error= "";
        self.flow_variations = [];
      },
      clear_flow(){
        let self = this;
        self.clear_stage();
        self.current_stages = [];
        self.flow_variations = [];
        self.variation_validation_error = ""
      },
      add_stage(){
        let self = this;
        let stage_name = document.getElementById("nt-stage-name");
        let bot_message = document.getElementById("nt-bot-says");
        let bot_greeting = "";
        let user_input = "";
        let user_input_type = "";
        if(bot_message.value==""){
          self.bot_says_error="This field cannot be blank!";
          return;
        }
        if(self.user_input_type=="Text + Buttons"){
          if(self.user_input_buttons.length==0){
            self.bot_buttons_error="This field cannot be blank!";
            return;
          }
        }
        if(self.user_input_type=="Text + Carousels"){
          if(self.user_input_carousels.length==0){
            self.bot_carousels_error="This field cannot be blank!";
            return;
          }
        }
        if(self.user_input_type=="Text"){
          user_input = "text";
          user_input_type = ['text'];
        }else if(self.user_input_type=="Text + Buttons"){
          user_input = self.user_input_buttons;
          user_input_type = 'buttons';
          self.user_input_buttons = [];
        }else if(self.user_input_type=="Text + Carousels"){
          user_input = self.user_input_carousels;
          user_input_type = 'carousels';
          self.user_input_carousels = [];
        }
        if(self.current_stages.length==0&&self.is_bot_greetings){
          bot_greeting = document.getElementById("nt-bot-greeting").value;
          document.getElementById("nt-bot-greeting").value = "";
        }
        let data = {
          stage_name: stage_name.value,
          bot_message: bot_message.value,
          bot_greeting: bot_greeting,
          user_input: user_input,
          user_input_type: user_input_type,
          input_validation: self.user_validation,
          input_validation_type: self.user_validation_type_,
          input_valid_next: self.user_valid_next,
          invalid_message: self.invalid_message
        }
        bot_message.value = "";
        stage_name.value = "";
        self.current_stages.push(data);
        self.clear_stage();
      },
      add_flow(){
        let self = this;
        let flow_name = self.current_flow_name;
        let data = {
          name: flow_name,
          stages: self.current_stages,
          variation: self.flow_variations
        }
        if(self.flow_index_type=="new"){
          if(self.flow_variations.length==0){
            self.variation_validation_error = "Variations cannot be empty";
            UIkit.modal("#nt-variations").show();
          }else{
            self.flow.push(data);
            self.flow_index_type="exist";
          }
        }else{
          if(self.flow_variations.length==0){
            self.variation_validation_error = "Variations cannot be empty";
            UIkit.modal("#nt-variations").show();
          }else{
            self.flow[self.flow_index] = data;
          }
        }
      },
      save_changes(){
        let self = this;
        let csrf_key = document.getElementById("csrf_token");
        let project_key = document.getElementById("project_key");
        let project_name = document.getElementById("project_name");
        let project_hash = document.getElementById("project_hash");
        let user_key = document.getElementById("user_key");
        let data = {
          flow: self.flow,
          faq: self.faq,
          smalltalks: self.smalltalks,
          key: project_key.value,
          name: project_name.value,
          hash: project_hash.value,
        }
        console.log(data);
        const url = "http://127.0.0.1:8000/datamanager/"+project_hash.value+"/savedata/";
        const Http = new XMLHttpRequest();
        Http.open("POST", url, true);
        Http.setRequestHeader("token", user_key.value);
        Http.setRequestHeader("X-CSRFToken", csrf_key.value);
        Http.send(JSON.stringify(data));
        Http.onload = () =>{
          if (Http.status == 200) {
            console.log(Http.responseText)
          }
        };
      },
    }
});

window.onbeforeunload = () => {
  return false;
}
