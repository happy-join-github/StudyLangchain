function updateTextArea(value) {
    const value = 'abc'
    const element = document.querySelector("textarea")
    element.value = value;
    console.log('jsHook');
    console.log(element.value);
}

function getContent(title_index) {
    const title_isTrue = document.querySelectorAll("div[data-message-id]")
    if (title_isTrue.length > 0 && title_index<=title_isTrue.length) {
        return {'content':title_isTrue[title_index].textContent,'problem':title_isTrue[title_index-1].textContent};
    }else{
        return {"content":"error",'problem':title_isTrue[title_index-1].textContent}
    }
}