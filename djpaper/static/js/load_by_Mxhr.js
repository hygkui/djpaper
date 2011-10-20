MXHR_Script = 
{
	queuedScripts: new Array(),
	loadScriptXhrInjection:function(url,onload,b_order)
	{
		var i_Q = MXHR_Script.queuedScripts.length;
		
		// 对新加入的进行初始化
		if ( b_order ) 
		{
			var qScript = {response:null,onload:onload,done:false};
			MXHR_Script.queuedScripts[i_Q] = qScript;
		}
	
	    //建立xml http request.
		var xhrObj = MXHR_Script.getXHRObject();
		//设定当其状态为ready的时候执行如下动作
		xhrObj.onreadystatechange = function() 
		{
			if ( xhrObj.readyState == 4 ) 
			{
				if ( b_order ) 
				{
					MXHR_Script.queuedScripts[i_Q].reponse = xhrObj.responseText;
					MXHR_Script.injectScripts();
				}
				else 
				{
					eval( xhrObj.responseText );
					if ( onload ) 
					{
						onload();
					}
				}
			}
		};
		// 发送xml http request 对象
		xhrObj.open('GET',url,true);
		xhrObj.send('');
	},

	injectScripts: function() 
	{
		var len = MXHR_Script.queuedScripts.length;
		for ( var i = 0 ; i < len ; i++ )
		{
			var qScript = MXHR_Script.queuedScripts[i];
			if ( ! qScript.done )
			{
				if ( ! qScript.response )
				{
					// stop and wait for this response
					break ;
				}
				else
				{
					eval( qScript.response );
					if ( qScript.onload ) 
					{
						qScript.onload();
					}
					qScript.done = true;
				}
			}
		}
	},

	getXHRObject: function() 
	{
		var xhrObj = false ;
		try 
		{
			xhrObj = new XMLHttpRequest();
		}
		catch( e )
		{
			var aTypes = ["Msxml2.XMLHTTP.6.0","Msxml2.XMLHTTP.3.0","Msxml2.XMLHTTP","Microsoft.XMLHTTP"];
			var len = aTypes.length;
			for ( var i = 0 ; i < len ; i++ )
			{
				try 
				{
					xhrObj = new ActiveXObject( aTypes[i] );
				}
				catch( e )
				{
					continue;
				}
				break;
			}
		}
		finally
		{
			return xhrObj;
		}
	}
};
function init()
{
	alert("load ok");
};





