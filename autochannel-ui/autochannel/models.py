from autochannel import db

class Guild(db.Model):
    __tablename__ = 'guild'
    id = db.Column(db.Integer, primary_key=True)
    categories = db.relationship('Category', backref='guild', lazy=True)

    def __repr__(self):
        return f'Guild({self.id})'
    
    def get_categories(self):
        cats = {}

        for category in self.categories:
            cats[category.id] = {}
            cats[category.id]['name'] = category.name
            cats[category.id]['prefix'] = category.prefix
            cats[category.id]['enabled'] = category.enabled
        
        return cats

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.Integer, db.ForeignKey('guild.id'))
    name = db.Column(db.String(40), unique=False, nullable=False)
    enabled = db.Column(db.Boolean, default=False, nullable=False)
    prefix = db.Column(db.String(10), unique=False, nullable=False, default='AC!')
    
    def get_data(self):
        return jsonify(id=self.id, enabled=self.enabled, prefix=self.prefix)

    
    def __repr__(self):
        return f'category({self.id} {self.guild_id} {self.name} {self.enabled} {self.prefix})'