class EntriesController < ApplicationController
  protect_from_forgery with: :null_session
  
  def index
    @entries = Entry.order(:laptime)
    @entries_len = @entries.length 
  end
  
  def show
    @entry = Entry.find(params[:id])
  end

  def new
  end
  
  def edit
    @entry = Entry.find(params[:id])
  end
  
  def create
    @entry = Entry.new(entry_params)
	
    if @entry.save
	  redirect_to entries_path
	  
	  puts "I DID SOMETHING!"
	  
    else
      render 'index'
    end
  end
  
  def update
    @entry = Entry.find(params[:id])
	
    if @entry.update(entry_params)
      redirect_to entries_path
    else
      render 'edit'
    end
  end
  
  def destroy
    @entry = Entry.find(params[:id])
	@entry.destroy
	
	redirect_to entries_path
  end
  
  private
    def entry_params
	  params.require(:entry).permit(:user, :track, :vehicle, :laptime, :avgspeed, :lapnum)
	end
end
