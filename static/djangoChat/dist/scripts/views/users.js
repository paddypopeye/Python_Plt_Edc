define(["backbone","views/user"],function(e,t){return e.View.extend({el:".onlineUsers",initialize:function(){this.collection.fetch(),this.collection.on("add",this.render,this),this.collection.on("remove",this.render,this)},render:function(){return console.log("........................................rendering............"),this.$el.html(""),this.collection.each(this.addOne,this),this},addOne:function(e){var n=new t({model:e});this.$el.append(n.render().el)}})});