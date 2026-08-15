import axios from 'axios'

// All HTTP traffic goes through this one axios instance so the base URL,
// headers and (later) interceptors live in a single place. Components should
// import this rather than calling axios directly.
const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
})

export default client
