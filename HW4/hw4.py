from decimal import Decimal
from sqlalchemy import create_engine, String, Numeric, ForeignKey, select, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship, selectinload

engine = create_engine('sqlite:///hw4.db')

LocalSession = sessionmaker(
    bind=engine,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(10,2))
    in_stock: Mapped[bool] = mapped_column(default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))
    category: Mapped['Category'] = relationship(back_populates='products')

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, in_stock={self.in_stock}, category_id={self.category_id})>"

class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(255))
    products: Mapped[list['Product']] = relationship(back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, description={self.description})>"

Base.metadata.create_all(engine)

with LocalSession() as session:
    #---task1---
    electronics = Category(
        name="Электроника",
        description="Гаджеты и устройства."
    )
    books = Category(
        name="Книги",
        description="Печатные книги и электронные книги."
    )
    clothing = Category(
        name="Одежда",
        description="Одежда для мужчин и женщин."
    )
    sport = Category(
        name="Спорт",
        description="Спортивная одежда и инвентарь"
    )

    categories = [electronics, books, clothing, sport]

    products = [
        Product(
            name="Смартфон",
            price=Decimal("299.99"),
            in_stock=True,
            category=electronics
        ),
        Product(
            name="Ноутбук",
            price=Decimal("499.99"),
            in_stock=True,
            category=electronics
        ),
        Product(
            name="Научно-фантастический роман",
            price=Decimal("15.99"),
            in_stock=True,
            category=books
        ),
        Product(
            name="Джинсы",
            price=Decimal("40.50"),
            in_stock=True,
            category=clothing
        ),
        Product(
            name="Футболка",
            price=Decimal("20.00"),
            in_stock=True,
            category=clothing
        )
    ]

    session.add_all(categories)
    session.add_all(products)
    session.commit()

    #---task2---
    all_categories = session.scalars(
        select(Category).options(selectinload(Category.products))
    ).all()
    for category in all_categories:
        print(f"\nКатегория: {category.name}")
        for product in category.products:
            print(f"  - {product.name} | {product.price}")

    #---task3---
    smartphone = session.scalars(
        select(Product).where(Product.name == "Смартфон")
    ).first()

    if smartphone:
        smartphone.price = Decimal("349.99")
        session.commit()
        print(f"Новая цена смартфона: {smartphone.price}")

    #---task4---
    result = session.execute(
        select(
            Category.name,
            func.count(Product.id)
        )
        .outerjoin(Product)
        .group_by(Category.name)
    ).all()

    for category_name, count in result:
        print(f"{category_name}: {count} продуктов")

    #---task5---
    result = session.execute(
        select(
            Category.name,
            func.count(Product.id)
        )
        .outerjoin(Product)
        .group_by(Category.name)
        .having(func.count(Product.id) > 1)
    ).all()

    for category_name, count in result:
        print(f"{category_name}: {count} продуктов")