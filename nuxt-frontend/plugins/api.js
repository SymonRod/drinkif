import axios from 'axios'

const api = axios.create({
  baseURL: 'https://drinkif.serod.tech/api/',
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.log(error)
  }
)

export default api
