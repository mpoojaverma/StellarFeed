import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, NavLink } from 'react-router-dom';
import axios from 'axios';
import { TailSpin } from 'react-loader-spinner';

// Main App Component
const App = () => {
  const [apod, setApod] = useState(null);
  const [news, setNews] = useState([]);
  const [poems, setPoems] = useState([]);
  const [constellation, setConstellation] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // Fetch data from all API endpoints concurrently for better performance
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
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  return (
    <Router>
      <div className="bg-gray-900 text-gray-300 min-h-screen">
        <Navbar />
        <main className="pt-24 container mx-auto p-4">
          {loading ? (
            <div className="flex justify-center items-center h-96">
              <TailSpin color="#60a5fa" height={80} width={80} />
            </div>
          ) : (
            <Routes>
              <Route path="/" element={<HomePage apod={apod} poems={poems} constellation={constellation} />} />
              <Route path="/news" element={<NewsPage news={news} />} />
              <Route path="/poems" element={<PoemsPage poems={poems} />} />
              <Route path="/about" element={<AboutPage />} />
            </Routes>
          )}
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
        <NavLink to="/" className="flex items-center space-x-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="text-teal-400">
            <path d="M12 2L2 22h20L12 2z" />
            <path d="M12 5L5 19h14L12 5z" />
            <circle cx="12" cy="12" r="3" fill="#60a5fa"/>
          </svg>
          <span className="text-3xl font-extrabold text-white">StellarFeed</span>
        </NavLink>
        <div className="hidden md:flex space-x-8 text-lg font-semibold">
          <NavLink to="/news" activeclassname="text-teal-400" className="text-gray-300 hover:text-teal-400 transition-colors duration-300">News</NavLink>
          <NavLink to="/poems" activeclassname="text-teal-400" className="text-gray-300 hover:text-teal-400 transition-colors duration-300">Poems</NavLink>
          <NavLink to="/about" activeclassname="text-teal-400" className="text-gray-300 hover:text-teal-400 transition-colors duration-300">About</NavLink>
        </div>
      </div>
    </nav>
  );
};

// HomePage Component
const HomePage = ({ apod, poems, constellation }) => {
  const poem = poems[0] || { text: 'Loading...', author: 'StellarFeed' };
  return (
    <div className="pt-16">
      <h1 className="text-6xl font-extrabold text-center mb-10 text-white">Your Daily Dose of the Cosmos</h1>
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
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredNews, setFilteredNews] = useState(news);

  useEffect(() => {
    const results = news.filter(article =>
      article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      article.description.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredNews(results);
  }, [searchTerm, news]);

  if (news.length === 0) {
    return <div className="text-center py-16">No news available.</div>;
  }

  return (
    <div className="pt-16">
      <h1 className="text-6xl font-extrabold text-center mb-10 text-white">Latest Space News</h1>
      <div className="mb-8">
        <input
          type="text"
          placeholder="Search for articles..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full p-4 rounded-lg bg-gray-800 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
      </div>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {filteredNews.length > 0 ? (
          filteredNews.map((article, index) => (
            <a href={article.url} key={index} className="p-6 bg-gray-800 rounded-lg shadow-lg hover:shadow-xl">
              <img src={article.urlToImage} alt={article.title} className="rounded-lg mb-4 w-full h-48 object-cover" />
              <h2 className="text-2xl font-bold mb-2 text-teal-400">{article.title}</h2>
              <p className="text-sm">{article.description}</p>
            </a>
          ))
        ) : (
          <div className="col-span-full text-center p-16">
            <p className="text-xl">No articles found for your search.</p>
          </div>
        )}
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
      <h1 className="text-6xl font-extrabold text-center mb-10 text-white">Cosmic Poems</h1>
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
      <h1 className="text-6xl font-extrabold text-center mb-10 text-white">About StellarFeed</h1>
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
