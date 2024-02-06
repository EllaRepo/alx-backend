import express from 'express';
import { promisify } from 'util';
import { createClient } from 'redis';

const app = express();
const port = 1245;
const redisClient = createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);

const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
];

function getItemById(id) {
  return listProducts.find(item => item.itemId === id);
}

function reserveStockById(itemId, stock) {
  redisClient.set(itemId, stock);
}

async function getCurrentReservedStockById(itemId) {
  const stock = await getAsync(itemId);
  return stock;
}

app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);

  if (item) {
    const stock = await getCurrentReservedStockById(itemId);
    const currentQuantity = stock !== null ? parseInt(stock) : item.initialAvailableQuantity;
    const resItem = {
      itemId: item.itemId,
      itemName: item.itemName,
      price: item.price,
      initialAvailableQuantity: item.initialAvailableQuantity,
      currentQuantity
    };
    res.json(resItem);
  } else {
    res.json({ status: "Product not found" });
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);

  if (!item) {
    res.json({ status: "Product not found" });
    return;
  }

  let currentStock = await getCurrentReservedStockById(itemId);
  if (currentStock !== null) {
    currentStock = parseInt(currentStock);
    if (currentStock > 0) {
      reserveStockById(itemId, currentStock - 1);
      res.json({ status: "Reservation confirmed", itemId });
    } else {
      res.json({ status: "Not enough stock available", itemId });
    }
  } else {
    reserveStockById(itemId, item.initialAvailableQuantity - 1);
    res.json({ status: "Reservation confirmed", itemId });
  }
});

app.listen(port, () => {
  console.log(`app listening at http://localhost:${port}`);
});
