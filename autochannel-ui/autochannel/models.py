from sqlalchemy import Integer, ForeignKey, String, Column, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from autochannel.database import Base

class Guild(Base):
    __tablename__ = 'guild'
    id = Column(Integer, primary_key=True)
    categories = relationship('Category', backref='categories', lazy=True)

    def __repr__(self):
        return f'Guild({self.id})'
    
    def get_categories(self):
        cats = {}

        for category in self.categories:
            cats[category.id] = {}
            cats[category.id]['prefix'] = category.prefix
            cats[category.id]['enabled'] = category.enabled
        
        return cats

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, ForeignKey('guild.id'), nullable=False)
    enabled = Column(Boolean, default=False, nullable=False)
    prefix = Column(String(10), unique=False, nullable=False, default='AC!')
    
    def get_data(self):
        return jsonify(id=self.id, enabled=self.enabled, prefix=self.prefix)

    def __repr__(self):
        return f'category({self.id} {self.guild_id} {self.name} {self.enabled} {self.prefix})'