(function($) {
// save the original function object
var _superModal = $.fn.modal;

// // add locked as a new option
$.extend( _superModal.defaults, {
    locked: false
});

// create a new constructor
var Modal = function(element, options) {
    _superModal.Constructor.apply( this, arguments )
}

// extend prototype and add a super function
Modal.prototype = $.extend({}, _superModal.Constructor.prototype, {
    constructor: Modal, 

    _super: function() {
        var args = $.makeArray(arguments)
        // call bootstrap core
        _superModal.Constructor.prototype[args.shift()].apply(this, args)
    }, 

    lock : function() {
        this.options.locked = true
    }

    , unlock : function() {
        this.options.locked = false
    }
    
    , hide: function() {
        if (this.options.locked) return
        this._super('hide')
    }
});

$.fn.modal = function(option) {
    return this.each(function() {
        var $this = $(this);
        var data = $this.data('modal');
        var options = $.extend({}, _superModal.defaults, $this.data(), typeof option == 'object' && option);

        if(!data) $this.data('modal', (data = new Modal(this, options)));
        if(typeof option == 'string') data[option]()
        else if (options.show) data.show()
    }); 
};

})($);

