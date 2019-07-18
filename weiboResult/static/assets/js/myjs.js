//提交表单
function getinfo(that){
	let a = Date.now();
	console.log(a);
	 var trseq = $(that).parent().parent().find("tr").index($(that).parent()[0]);  
	console.log(that);
	console.log(trseq);
	var _label=document.getElementById("mytable").getElementsByTagName("tr")[trseq].getElementsByTagName("td")[0].innerHTML;
	console.log(_label);
	var _name = document.getElementById("mytable").getElementsByTagName("tr")[trseq].getElementsByTagName("td")[1].innerHTML;
	console.log(_name);
	var _Tag = document.getElementById("mytable").getElementsByTagName("tr")[trseq].getElementsByTagName("td")[2].innerHTML;
	console.log(_Tag);
	var _text = document.getElementById("mytable").getElementsByTagName("tr")[trseq].getElementsByTagName("td")[3].innerHTML;
	console.log(_text);
	// $('.box').html('<div>Success</div>');
	var data = {
		data:JSON.stringify({"label": _label, "name": _name,"_tag":_Tag,"text":_text})
	}
	$.ajax({
            url:'http://127.0.0.1:5000/update',
            type: 'POST',
        	data: data,
            success:function(data) {
            	let b = Date.now();
            	console.log(b);
                if (data.result == 1) {
                    alert("标签修改成功");
                   }

                else{
                	alert("标签修改失败");
                }
            }
        })
}

