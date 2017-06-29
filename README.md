# Warframe Market Tool

This tool uses [this](http://warframe.market) and [this](http://warframe.wikia.com) to make some awesome things.

Currently able to list items using (warframe.market's API).
  * Grabs lowest 10 buy and sell orders
  * Dynamically grabs pictures and links for each item's page

Registration is fully implemented
  * Orders can only be placed by logged-in users
    * These users must also have entered in valid warframe.market credentials

Any User's Orders can be accessed at **/orders/[USERNAME]**

Auto Orders!
  * Just enter in an item name and it will automatically adjust the price, plat, quantity
  * Orders can be placed on item pages as-well

# TODO
 * Potentially expand to Rivens?
