//
//  TableViewCell.swift
//  ZTI_app
//
//  Created by Adam Linke on 09/01/2019.
//  Copyright © 2019 Adam Linke. All rights reserved.
//

import Foundation
import UIKit

class TableViewCell: UITableViewCell {
    
    @IBOutlet weak var nameLabel: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }
    
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
        // Configure the view for the selected state
    }
    
    func update(with result: String) {
        nameLabel.text = result
        //print("UPDATE")
    }
    
}
