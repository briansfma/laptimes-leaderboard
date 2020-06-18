class CreateEntries < ActiveRecord::Migration[6.0]
  def change
    create_table :entries do |t|
      t.string :user
      t.string :track
      t.string :vehicle
      t.string :laptime
      t.string :avgspeed
      t.string :lapnum

      t.timestamps
    end
  end
end
