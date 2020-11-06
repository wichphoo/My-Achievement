library(randomForest)
library(caret)

set.seed(1234)

#import data
AccData <- read.csv("C:/Users/Windows/Dropbox/R-Code/RandomForest/AccData.csv")

#split into traindata 80%, testdata 20%
idx <- sample(nrow(AccData), 0.8*nrow(AccData))
traindata <- AccData[idx, ]
testdata <- AccData[-idx, ]

#tuning model
  fitControl <- trainControl(
  ## Repeated 5-fold CV 
  method = "repeatedcv",
  number = 5,
  ## repeated 5 times
  repeats = 5,
  verboseIter = TRUE,
  returnResamp = "all")

RF_fit <- train(Tc ~ ., 
          data = traindata,
          method = 'ranger',
          # should be set high at least p/3
          tuneLength = 15, 
          trControl = fitControl,
          ## parameters passed onto the ranger function
          # the bigger the better.
          num.trees = 500,
          importance = "permutation")

plot(RF_fit) #show fitting mtry = 5, splitrule = extratrees

#plot ntree from another package (can skip)
library(randomForest)
RF_tree <- randomForest(Tc ~., data=traindata,
                   ntree = 500,
                   mtry = 6,
                   importance = TRUE,
                   proximity = TRUE)

#test performance of model
library(Metrics)
RF_predict <- predict(RF_fit, testdata)
mae(testdata$Tc, RF_predict)
rmse(testdata$Tc, RF_predict)
mape(testdata$Tc, RF_predict)*100

#see importance variable
varImp(RF_fit)
plot(varImp(RF_fit), top = 20)

#prediction chart
plot(RF_predict, testdata$Tc, xlab = "Predicted", ylab = "Actual", cex.lab=2, cex.axis=2, xlim = c(0,250), ylim = c(0,250))
abline(1,1, col = "red")



