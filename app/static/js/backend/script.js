$(document).ready(function(){
		// Convert parcentage to coeff
		function to_percent(num){
			return (num / 100) + 1
		}
		// Price is before tax, vat is in percentage format
		function price_after_tax (price, vat) {
			return price * to_percent(vat)
		}
		// Compute Gross Margin as Percentage
		function gross_margin(selling, buying) {
			return ((selling - buying) / buying) * 100
		}
		// Compute selling Price from Buying Price and Margin as a percentage
		function selling(buying, margin) {
			return buying * to_percent(margin)
		}

		// Update Selling Price when VAT is changed
		$('#vat').change(function(){
			var price = price_after_tax($('#selling_price_no_tax').val(), $('#vat option:selected').text())
			$('#price').val(price.toFixed(2));
		});

		// Initialize the values on load
		var margin = gross_margin($('#selling_price_no_tax').val(), $('#buying_price').val())
        $('#margin').val(margin.toFixed(2));
        var price = price_after_tax($('#selling_price_no_tax').val(), $('#vat option:selected').text())
        $('#price').val(price.toFixed(2));

        // Compute Margin from Selling Price
	    $('#selling_price_no_tax').keyup(function(){
	    	var margin = gross_margin($('#selling_price_no_tax').val(), $('#buying_price').val())
	        $('#margin').val(margin.toFixed(2));
	        var price = price_after_tax($('#selling_price_no_tax').val(), $('#vat option:selected').text())
	        $('#price').val(price.toFixed(2));
	    });

	    // Compute Selling Price from Margin
	    $('#margin').keyup(function(){
	    	var selling_price = selling($('#buying_price').val(), $('#margin').val())
	        $('#selling_price_no_tax').val(selling_price.toFixed(2));
	        var price = price_after_tax($('#selling_price_no_tax').val(), $('#vat option:selected').text())
	        $('#price').val(price.toFixed(2));
	    });

	    // Compute Selling Price from Buying Price, Margin being unchanged
	    $('#buying_price').keyup(function(){
	    	var selling_price = selling($('#buying_price').val(), $('#margin').val())
	        $('#selling_price_no_tax').val(selling_price.toFixed(2));
	        var price = price_after_tax($('#selling_price_no_tax').val(), $('#vat option:selected').text())
	        $('#price').val(price.toFixed(2));
	    });
	});