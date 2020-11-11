#import data
AccData <- read.csv("C:/Users/Windows/Dropbox/R-Code/RandomForest/AccData.csv")

#split into traindata 80%, testdata 20%
idx <- sample(nrow(AccData), 0.8*nrow(AccData))
traindata <- AccData[idx, ]
testdata <- AccData[-idx, ]
 
#built decision tree model
library(rpart)
library(rpart.plot)
DT_model <- rpart(Tc ~ ., data = traindata, method = "anova")

#plot model
rpart.plot(DT_model)

#show cp & nsplit must built model with deep cp
DT_cp <- rpart(Tc ~ ., data = AccData, method = "anova", cp=0.001)
plotcp(DT_model)
printcp(DT_model)

#model performance
library(Metrics)
DT_predict <- predict(DT_model, testdata)
mae(testdata$Tc, DT_predict)
rmse(testdata$Tc, DT_predict)
mape(testdata$Tc, DT_predict)*100

#prediction chart
plot(DT_predict, testdata$Tc, xlab = "Predicted", ylab = "Actual", cex.lab=2, cex.axis=2, xlim = c(0,250), ylim = c(0,250))
abline(1,1, col = "red")

