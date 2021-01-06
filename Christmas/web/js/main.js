//前回検索条件
pre_conditon = {}

eel.expose(js_function)
function js_function(values) {
    pre_conditon = values
    console.log(values)
    //前回検索条件を反映
    //　 {"email": "", "password": "", "name": "", "url": ""}
    $("#lancers_text").val(pre_conditon["name"])
    $("#lancers_hidden").val(pre_conditon["url"])
    $("#lancers_email").val(pre_conditon["email"])
    $("#lancers_password").val(pre_conditon["password"])
    if(pre_conditon["sort"]){
        $("#select1a").val(pre_conditon["sort"])
    }
    
    if(pre_conditon["url"]){
        // dropdown-menuクラスの下のaタグを対象に検索
        $.each($(".dropdown-menu a"), function(index, value){
            $a = $(this);
            if(pre_conditon["url"] == $a.attr("url")){
                $a.click();

            }
        });
    }
    
}
let loading = "<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span>Searching..."

// 検索後の共通処理
function search_after_common(returnVal, targetNum, word1){
    if(returnVal["result"] == "ok") {
        // 正常
        $("#result" + targetNum).text("検索条件："+ word1 );
        $("#result" + targetNum).append(document.createElement('br'))
        $("#result" + targetNum).append(returnVal["message"])
        $("#result" + targetNum).append(document.createElement('br'))
        $("#result" + targetNum).append(returnVal["detail"])
        $("#error" + targetNum).text("");
        $("#result" + targetNum).show();
        $("#error" + targetNum).hide();
    } else { 
        // エラー
        $("#result" + targetNum).text("");
        $("#error" + targetNum).text(returnVal["message"]);
        $("#result" + targetNum).hide();
        $("#error" + targetNum).show();
    }
    // 結果行を表示
    $("div[id^='result']").closest("tr").show();
    
    $("#search_button" + targetNum).attr("disabled",false);
    $("#search_button" + targetNum).html("検索")
}


// ランサーズ案件検索(server呼び出し)
async function search_lancers() {
    let word1 = $("#lancers_hidden").val();
    let word2 = $("#lancers_text").val();
    $("#search_button_lancers").attr("disabled",true);
    $("#search_button_lancers").html(loading);
    
    let param = {"name": $("#lancers_text").val(),
                "email": $("#lancers_email").val(),
                "password": $("#lancers_password").val(),
                "sort": $("#select1a").val(),
                }
    let val = await eel.search_lancers(word1, param)();
    search_after_common(val, "_lancers", $("#lancers_text").val());
}


// クラウドワークス案件検索(server呼び出し)
async function search_crowdworks() {
    let word1 = $("#crowdworks_hidden").val();
    let word2 = false;
    $("#search_button_crowdworks").attr("disabled",true);
    $("#search_button_crowdworks").html(loading)
    
    let param = {"name": $("#crowdworks_text").val(),
                "name2": $("#crowdworks_text").val(),
                "name3": $("#crowdworks_text").val(),
                }
    let val = await eel.search_crowdworks(word1, param)();
    search_after_common(val, "_crowdworks", $("#crowdworks_text").val());
}

// カテゴリのドロップダウン作成
function create_dropdown(target, val){
    let category_str = "";
    $.each(val[target], function(index, value){
        category_str = category_str + "<a class='dropdown-item' "
                    +"val='" + value["id"] + "' "
                    +"parent='" + value["parent"] + "' "
                    +"url='" + value["url"] + "' "
                    +"href='#'>"
                    + value["name"] +"</a>"
    });
    
    $("#select_"+target).html(category_str);
};

// カテゴリ検索
function search_category() {
    let val = lancers_category;
    create_dropdown("parent", val)
    create_dropdown("child", val)
    create_dropdown("grandchild", val)
    return val;
}
        
// カテゴリのドロップダウン作成 
function create_crowdworks_dropdown(target, val){
    let category_str = "";
    $.each(val[target], function(index, value){
        category_str = category_str + "<a class='dropdown-item' "
                    +"val='" + value["id"] + "' "
                    +"parent='" + value["parent"] + "' "
                    +"url='" + value["url"] + "' "
                    +"href='#'>"
                    + value["name"] +"</a>"
    });
    
    $("#select_crowdworks_"+target).html(category_str);
};

// カテゴリ検索
function search_crowdworks_category() {
    let val = crowdworks_category;

    create_crowdworks_dropdown("parent", val)
    create_crowdworks_dropdown("child", val)
    create_crowdworks_dropdown("grandchild", val)
    return val;
}

        

// ready後の処理
$(document).ready(function(){
    // カテゴリのドロップダウンを作成
    search_category();    
    search_crowdworks_category();

    //　初期表示
    $("div[id^='result']").hide();
    $("div[id^='error']").hide();
    $("div[id^='result']").closest("tr").hide();

    //　ナビのクリック処理
    $(".nav-link").on('click', function() {
      // 検索エリアの全消し
      $("div[id^='div']").hide();
      //　ナビの全消し
      $(".nav-link").removeClass("active");
      // 対象の検索エリア
      show_target = "#div" + $(this).attr("val");
      $(show_target).show();
      $(this).addClass("active");
      return
    });
    
    // ランサーズ検索
    $("#search_button_lancers").on('click', function() {
      if($("#lancers_hidden").val()==""){
        alert("カテゴリを選択してください");
        return
      }
      search_lancers();
      return
    });
    
    // クラウドワークス検索
    $("#search_button_crowdworks").on('click', function() {
      if($("#crowdworks_hidden").val()==""){
        alert("カテゴリを選択してください");
        return
      }
      search_crowdworks();
      return
    });
    

    let parent_button_text = "親カテゴリ";
    let child_button_text = "子カテゴリ";
    let grand_child_button_text = "孫カテゴリ";
    let selected_class = "btn-primary";
    let nonselect_class = "btn-secondary";
    // 親カテゴリのクリック処理
    $(".dropdown_parent").on("click", ".dropdown-item", function() {
      // 
      let parent_id = $(this).attr("val");
      $tr = $(this).closest("tr");
      $table = $(this).closest("table");
      // 子へ
      let $child = $(".dropdown_child", $tr)
      let targets = $(".dropdown-item", $child)
      $.each(targets, function(index, value){
          if($(value).attr("parent") == parent_id) {
              $(value).show();
          } else {
              $(value).hide();
          }
      });
      // 孫は全非表示
      $(".dropdown-item" ,$(".dropdown_grandchild", $tr)).hide();
      // 入力欄
      $("input[type='text']", $table).val($(this).text());
      $("input[type='hidden']", $table).val($(this).attr("url"));
      // ドロップダウンへ
      $(".dropdown_parent button", $tr).text($(this).text());
      $(".dropdown_parent button", $tr).removeClass(nonselect_class);
      $(".dropdown_parent button", $tr).addClass(selected_class);
      $(".dropdown_child button", $tr).text(child_button_text);
      $(".dropdown_child button", $tr).removeClass(selected_class);
      $(".dropdown_child button", $tr).addClass(nonselect_class);
      $(".dropdown_grandchild button", $tr).text(grand_child_button_text);
      $(".dropdown_grandchild button", $tr).removeClass(selected_class);
      $(".dropdown_grandchild button", $tr).addClass(nonselect_class);
      return
    });
            
    // 子カテゴリのクリック処理
    $(".dropdown_child").on("click", ".dropdown-item", function() {
      // 
      let child_id = $(this).attr("val");
      $tr = $(this).closest("tr");
      $table = $(this).closest("table");
      // 孫へ
      let targets = $(".dropdown-item" ,$(".dropdown_grandchild", $tr))
      $.each(targets, function(index, value){
      
          
          if($(value).attr("parent") == child_id) {
              $(value).show();
          } else {
              $(value).hide();
          }
      });
      $("input[type='text']", $table).val($(this).text());
      $("input[type='hidden']", $table).val($(this).attr("url"));
      // ドロップダウンへ
      $(".dropdown_child button", $tr).text($(this).text());
      $(".dropdown_child button", $tr).removeClass(nonselect_class);
      $(".dropdown_child button", $tr).addClass(selected_class);
      $(".dropdown_grandchild button", $tr).text(grand_child_button_text);
      $(".dropdown_grandchild button", $tr).removeClass(selected_class);
      $(".dropdown_grandchild button", $tr).addClass(nonselect_class);
      return
    });

    // 孫カテゴリのクリック処理
    $(".dropdown_grandchild").on("click", ".dropdown-item", function() {
      $tr = $(this).closest("tr");
      $table = $(this).closest("table");
      $("input[type='text']", $table).val($(this).text());
      $("input[type='hidden']", $table).val($(this).attr("url"));
      // ドロップダウンへ
      $(".dropdown_grandchild button", $tr).text($(this).text());
      $(".dropdown_grandchild button", $tr).removeClass(nonselect_class);
      $(".dropdown_grandchild button", $tr).addClass(selected_class);
    });
    
    
    //　ファンクションを追加後にする初期表示
    //　ナビ左端をクリック
    $(".nav-link")[0].click();
    


});