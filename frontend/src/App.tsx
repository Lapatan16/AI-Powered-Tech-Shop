import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './App.css'
import HomePage from './pages/homePage/homePage';
import ProductDetailPage from './pages/productDetailsPage/productDetailsPage';
import { Header } from './components/header/header';
import { AuthPage } from './pages/authPage/authPage';
import { NotFoundPage } from './pages/notFoundPage/notFoundPage';
import { CartPage } from './pages/cartPage/cartPage';
import { RecommendationsPage } from './pages/recommendationsPage/recommendationsPage';
import { CreateProductPage } from './pages/createProductPage/createProductPage';
import { DashboardPage } from './pages/dashboardPage/dashboardPage';

function App() {

  return(
    <>
      <BrowserRouter>
        <Header />
        
        <Routes>
          <Route path='/' element={<HomePage />}></Route>
          <Route path='/products/:id' element={<ProductDetailPage />}></Route>
          <Route path='/login' element={<AuthPage />}></Route>
          <Route path='/register' element={<AuthPage />}></Route>
          <Route path='/cart' element={<CartPage />}></Route>
          <Route path='/recommendations' element={<RecommendationsPage />}></Route>
          <Route path='/create-product' element={<CreateProductPage />}></Route>
          <Route path='/dashboard' element={<DashboardPage />}></Route>

          <Route path='*' element={<NotFoundPage />} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App