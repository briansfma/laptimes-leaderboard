Rails.application.routes.draw do
  get 'entries/index'
  
  resources :entries
  
  root 'entries#index'
end
