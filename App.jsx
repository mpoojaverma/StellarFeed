import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch, NavLink } from 'react-router-dom';
import axios from 'axios';

// Main App Component
const App = () => {
  const [apod, setApod] = useState(null);
  const [news, setNews] = useState([]);
  const [poems, setPoems] = useState([]);
  const [constellation, setConstellation] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [apodRes, newsRes, poemsRes, constellationRes] = await Promise.all([
        axios.get('/api/apod'),
        axios.get('/api/news'),
        axios.get('/api/poems'),
        axios.get('/api/constellation'),
      ]);
      setApod(apodRes.data);
      setNews(newsRes.data);
      setPoems(poemsRes.data);
      setConstellation(constellationRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <Router>
      <div className="bg-gray-900 text-gray-300 min-h-screen">
        <Navbar />
        <main className="pt-24 container mx-auto">
          <Switch>
            <Route path="/" exact>
              <HomePage apod={apod} poems={poems} constellation={constellation} />
            </Route>
            <Route path="/news">
              <NewsPage news={news} />
            </Route>
            <Route path="/poems">
              <PoemsPage poems={poems} />
            </Route>
            <Route path="/about">
              <AboutPage />
            </Route>
          </Switch>
        </main>
      </div>
    </Router>
  );
};

// Navbar Component
const Navbar = () => {
  return (
    <nav className="bg-gray-900 bg-opacity-80 backdrop-filter backdrop-blur-lg p-4 shadow-lg fixed w-full z-10">
      <div className="container mx-auto flex justify-between items-center">
        <a href="/" className="flex items-center space-x-4">
          <span className="text-3xl font-extrabold text-white">StellarFeed</span>
        </a>
        <div className="hidden md:flex space-x-8 text-lg font-semibold">
          <NavLink to="/news" activeClassName="text-teal-400" className="text-gray-300 hover:text-teal-400 transition-colors duration-300">News</NavLink>
          <NavLink to="/poems" activeClassName="text-teal-400" className="text-gray-300 hover:text-teal-400 transition-colors duration-300">Poems</NavLink>
          <NavLink to="/about" activeClassName="text-teal-400" className="text-gray-300 hover:text-teal-400 transition-colors duration-300">About</NavLink>
        </div>
      </div>
    </nav>
  );
};

// HomePage Component
const HomePage = ({ apod, poems, constellation }) => {
  if (!apod || !constellation || poems.length === 0) {
    return <div className="text-center py-16">Loading...</div>;
  }
  const poem = poems[0]; // Show a random poem
  return (
    <div className="pt-16">
      <h1 className="text-6xl font-extrabold text-center mb-10">Your Daily Dose of the Cosmos</h1>
      <section className="p-8 my-10 bg-gray-800 rounded-lg shadow-lg">
        <h2 className="text-4xl font-bold mb-6 text-teal-400">{apod.title}</h2>
        <img src={apod.url} alt={apod.title} className="rounded-lg mb-6 w-full h-auto object-cover" />
        <p className="text-lg">{apod.explanation}</p>
      </section>
      <section className="p-8 my-10 bg-gray-800 rounded-lg shadow-lg">
        <h2 className="text-4xl font-bold mb-6 text-cyan-400">Poem of the Day</h2>
        <p className="text-xl italic">"{poem.text}"</p>
        <p className="mt-4 text-right">- {poem.author}</p>
      </section>
    </div>
  );
};

// NewsPage Component
const NewsPage = ({ news }) => {
  if (news.length === 0) {
    return <div className="text-center py-16">No news available.</div>;
  }
  return (
    <div className="pt-16">
      <h1 className="text-6xl font-extrabold text-center mb-10">Latest Space News</h1>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {news.map((article, index) => (
          <a href={article.url} key={index} className="p-6 bg-gray-800 rounded-lg shadow-lg hover:shadow-xl">
            <img src={article.urlToImage} alt={article.title} className="rounded-lg mb-4 w-full h-48 object-cover" />
            <h2 className="text-2xl font-bold mb-2 text-teal-400">{article.title}</h2>
            <p className="text-sm">{article.description}</p>
          </a>
        ))}
      </div>
    </div>
  );
};

// PoemsPage Component
const PoemsPage = ({ poems }) => {
  if (poems.length === 0) {
    return <div className="text-center py-16">No poems available.</div>;
  }
  return (
    <div className="pt-16">
      <h1 className="text-6xl font-extrabold text-center mb-10">Cosmic Poems</h1>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {poems.map((poem, index) => (
          <div key={index} className="p-6 bg-gray-800 rounded-lg shadow-lg">
            <p className="text-xl italic">"{poem.text}"</p>
            <p className="mt-4 text-right">- {poem.author}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

// AboutPage Component
const AboutPage = () => {
  return (
    <div className="pt-16">
      <h1 className="text-6xl font-extrabold text-center mb-10">About StellarFeed</h1>
      <section className="p-8 my-10 bg-gray-800 rounded-lg shadow-lg">
        <h2 className="text-4xl font-bold mb-4 text-teal-400">Our Mission</h2>
        <p className="text-lg">StellarFeed is a web application designed to bring you a daily collection of cosmic content.</p>
      </section>
      <section className="p-8 my-10 bg-gray-800 rounded-lg shadow-lg">
        <h2 className="text-4xl font-bold mb-4 text-teal-400">API Integrations</h2>
        <ul className="list-disc list-inside text-lg">
          <li>NASA Astronomy Picture of the Day (APOD)</li>
          <li>NewsAPI.org</li>
          <li>Google Gemini API</li>
        </ul>
      </section>
    </div>
  );
};

export default App;

