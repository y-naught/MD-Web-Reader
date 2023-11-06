function linkTOC(){
    window.location="contents"
}

function linkHome(){
    window.location="/"
}

let side_nav_container = document.getElementById("side_nav");

let side_nav_expanded = false
function toggle_side_nav(){
    if(!side_nav_expanded){
        // Run some transformation on the side nav bar
        side_nav_container.classList.add("show_nav");
        side_nav_expanded = true;
    }else{
        // Run the opposite transformation on the side nav bar
        side_nav_container.classList.remove("show_nav");
        side_nav_expanded = false;
    }
}

// Top nav buttons
let toc_div = document.getElementById("toc_top_nav_container");
let home_div = document.getElementById("home_top_nav_container");
let contents_img = document.getElementById("toc_toggle_svg");


// Top nav button listeners
toc_div.addEventListener("click", function() { 
    linkTOC();
});

home_div.addEventListener("click", function(){
    linkHome();
});

contents_img.addEventListener("click", () => {
    toggle_side_nav();
})


// hide top nav on scroll
let main_container = document.getElementById("main_content_container");
let top_nav_container = document.getElementById("top_nav")
let scroll_direction = true;

let cog_nav_container = document.getElementById("settings_cog_nav_container");
let cog_image = document.getElementById("settings_cog_svg");
let settings_window = document.getElementById("settings_window");
let settings_toggle = true;



function scrollHandler(event){
    // False for scrolling down, True for scrolling up
    if(event.deltaY > 0){
        if(scroll_direction == true){
            top_nav_container.classList.add("hide_nav");
            settings_window.classList.remove("show_window");
            side_nav_container.classList.remove("show_nav");
            settings_toggle = true;
            side_nav_expanded = false;
        }
        scroll_direction = false;
    }else{
        if(scroll_direction == false){
            top_nav_container.classList.remove("hide_nav");
        }
        scroll_direction = true;
    }
}

main_container.addEventListener("wheel", scrollHandler, {passive: true})

// Sets pop-in settings window height
let nav_height = top_nav_container.offsetHeight;
console.log("nav height : ", nav_height);


// Handles Settings window
function toggle_settings_window(){
    if(settings_toggle){
        settings_toggle = false;
        settings_window.classList.add("show_window");
        cog_image.classList.add("settings_cog_rotate");
        console.log("Show window");
    }
    else{
        settings_toggle = true;
        settings_window.classList.remove("show_window");
        cog_image.classList.remove("settings_cog_rotate");
        console.log("hide window");
    }
}

cog_nav_container.addEventListener("click", toggle_settings_window)

settings_window.style.top = nav_height.toString() + 'px'
side_nav_container.style.top = nav_height.toString() + 'px'


// Handles the font size slider 
let font_slider = document.getElementById("font_slider")
let font_size_display = document.getElementById("font_size_display")

main_stylesheet = getStyleSheets();

font_size_display.innerHTML = font_slider.value;
font_value = font_slider.value

font_slider.addEventListener("input", () => {
    font_value = font_slider.value;
    font_size_display.innerHTML = font_value;
    updateFontCSS(main_stylesheet, font_value, 6, 20);
})

function getStyleSheets(){
    for(let i = 0; i < document.styleSheets.length; i++){
        let sheet = document.styleSheets[i];
        if(sheet.title == "section_styles"){
            console.log(sheet.cssRules);
            return sheet;
        }
    }
    return null;
}

function calcFontSize(newSize, min, max){
    let normalized_val = newSize / (max - min);
    console.log("normalized_val :", normalized_val);
    let remMin = 0.8;
    let remMax = 1.5;
    let newVal = normalized_val * (remMax - remMin) + remMin;
    let remVal = newVal.toString() + "rem";
    return remVal;
}

function updateFontCSS(stylesheet, newSize, min, max){
    
    //scale paragraphs
    pRuleIndex = 13;
    updatedPFont = calcFontSize(newSize, min, max);
    newParagraphRule = "p, li {font-size: " + updatedPFont + "; margin-top: 0.5rem; margin-bottom: 0.5rem}";
    stylesheet.deleteRule(pRuleIndex);
    stylesheet.insertRule(newParagraphRule, pRuleIndex);
    
    //scale headers
    header_rule_indices = [8,9,10,11,12]
    header_default_sizes = [1.9,1.8,1.7,1.6,1.5]
    
    for(let i = 0; i < header_rule_indices.length; i++){
        stylesheet.deleteRule(header_rule_indices[i]);
        multiplier = 0.05;
        hSize = (newSize - min) * multiplier + header_default_sizes[i];
        newHRule = "h" + (i+2).toString() + " {font-size: " + hSize.toString() + "rem}";
        stylesheet.insertRule(newHRule, header_rule_indices[i]);
    }

    //scale latex
    let latexScaleMin = 1.0;
    let latexScaleMultiplier = 0.1;
    let latexScale = (newSize - min) * latexScaleMultiplier + latexScaleMin;
    
    let latexRuleIndex = 14;
    stylesheet.deleteRule(14);
    
    let newLatexRule = ".MathJax { font-size: " + latexScale.toString() + "rem !important; }";
    stylesheet.insertRule(newLatexRule, latexRuleIndex);
}

updateFontCSS(main_stylesheet, font_slider.value, 6, 20);

// handles dark mode
darkMode = false;
function toggleDarkModeCSS(stylesheet){
    if(!darkMode){
        num_CSS_Rules = stylesheet.cssRules.length;
        darkMode = true;
        // add in darkmode rules to bottom of css list
        font_color_rule = "h1, h2, h3, h4, h5, h6, p, li, a, .sub_section_link {color: white}";
        stylesheet.insertRule(font_color_rule, num_CSS_Rules);
        background_color_rule = "body, main {background-color: black}";
        stylesheet.insertRule(background_color_rule, num_CSS_Rules + 1);
        top_bar_color_rule = "#top_nav, #settings_window, #side_nav {background-color: rgba(5,5,5,0.95);}"
        stylesheet.insertRule(top_bar_color_rule, num_CSS_Rules + 2);
        mathjax_rule = ".MathJax {color: white;}"
        stylesheet.insertRule(mathjax_rule, num_CSS_Rules + 3);
        hover_rule = ".top_nav_links:hover{background-color: #444444;}"
        stylesheet.insertRule(hover_rule, num_CSS_Rules + 4);
    }else{
        darkMode = false;
        num_CSS_Rules = stylesheet.cssRules.length;
        num_rules = 5;
        // remove the rules
        for(let i = 1; i <= num_rules; i++){
            stylesheet.deleteRule(num_CSS_Rules - i);
        }
    }
}

let darkmode_checkbox = document.getElementById("dark_mode_input");

if(darkmode_checkbox.checked == true){
    toggleDarkModeCSS(main_stylesheet);
}

darkmode_checkbox.addEventListener("input", () => {
    toggleDarkModeCSS(main_stylesheet);
    console.log("toggled darkmode!");
});