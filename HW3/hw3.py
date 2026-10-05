from decimal import Decimal
from sqlalchemy import String, Boolean, create_engine, ForeignKey,Numeric
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase, relationship

engine = create_engine('sqlite:///:memory:')

LocalSession = sessionmaker(
    bind=engine,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(10,2))
    in_stock: Mapped[bool] = mapped_column(Boolean)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))
    category: Mapped['Category'] = relationship(back_populates='products')

    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price}, in_stock={self.in_stock}, category_id={self.category_id})>"

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    products: Mapped[list[Product]] = relationship(back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Category(name={self.name}, description={self.description})>"


Base.metadata.create_all(engine)

with LocalSession() as session:
    fruits = Category(
        name='Fruits',
        description='Fresh and delicious fruits'
    )

    vegetables = Category(
        name='Vegetables',
        description='Fresh vegetables for every meal'
    )

    apple = Product(
        name='Apple',
        price=Decimal('1.99'),
        in_stock=True
    )

    banana = Product(
        name='Banana',
        price=Decimal('2.49'),
        in_stock=True
    )

    carrot = Product(
        name='Carrot',
        price=Decimal('0.99'),
        in_stock=True
    )

    cucumber = Product(
        name='Cucumber',
        price=Decimal('1.49'),
        in_stock=False
    )

    fruits.products.append(apple)
    fruits.products.append(banana)

    vegetables.products.append(carrot)
    vegetables.products.append(cucumber)

    session.add(fruits)
    session.add(vegetables)

    session.commit()

print(fruits)
print(fruits.products)

print(vegetables)
print(vegetables.products)