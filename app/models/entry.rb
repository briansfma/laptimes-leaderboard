class Entry < ApplicationRecord
  validates :track, presence: true,
                    length: { minimum: 2 }
  validates :laptime, presence: true,
                    length: { minimum: 2 }
  validates :lapnum, presence: true,
                     uniqueness: true
end
